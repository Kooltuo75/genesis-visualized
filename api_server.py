"""
Genesis Frame Editor API Server
================================
Provides API endpoints for editing frames from the web visualizer.
Now with user authentication and cloud deployment support.

Run: python api_server.py
API runs on port 8003, static files on port 8005
"""

import json
import os
import sys
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from datetime import datetime
import threading

# Import authentication module
import auth

# Cloudinary import (optional - only if using cloud storage)
try:
    import cloudinary
    import cloudinary.uploader
    CLOUDINARY_AVAILABLE = True
except ImportError:
    CLOUDINARY_AVAILABLE = False

# Configure UTF-8 for Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

DATABASE_FILE = "frames-database.json"
IMAGES_DIR = Path("images")
API_PORT = int(os.environ.get('PORT', 8003))  # Support Render's PORT env var
STATIC_PORT = int(os.environ.get('STATIC_PORT', 8005))

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def load_database():
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_env_var(var_name):
    """Load a single environment variable from .env file."""
    # First check system environment variables (for Render deployment)
    if var_name in os.environ:
        return os.environ[var_name]

    # Fall back to .env file
    env_path = Path('.env')
    if not env_path.exists():
        return None
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith(f'{var_name}='):
                return line.strip().split('=', 1)[1]
    return None

def load_api_key():
    return load_env_var('OPENAI_API_KEY')

def setup_cloudinary():
    """Configure Cloudinary if credentials are available."""
    if not CLOUDINARY_AVAILABLE:
        print("Cloudinary not installed. Using local storage only.")
        return False

    cloud_name = load_env_var('CLOUDINARY_CLOUD_NAME')
    api_key = load_env_var('CLOUDINARY_API_KEY')
    api_secret = load_env_var('CLOUDINARY_API_SECRET')
    use_cloudinary = load_env_var('USE_CLOUDINARY')

    if use_cloudinary != 'true':
        print("Cloudinary disabled (USE_CLOUDINARY != 'true'). Using local storage.")
        return False

    if not all([cloud_name, api_key, api_secret]) or cloud_name == 'your_cloud_name':
        print("Cloudinary credentials not configured. Using local storage.")
        return False

    cloudinary.config(
        cloud_name=cloud_name,
        api_key=api_key,
        api_secret=api_secret
    )
    print(f"Cloudinary configured: {cloud_name}")
    return True

# Initialize Cloudinary on startup
USE_CLOUD_STORAGE = setup_cloudinary() if CLOUDINARY_AVAILABLE else False

def get_frame_by_id(frame_id):
    data = load_database()
    for frame in data['frames']:
        if frame['id'] == frame_id:
            return frame, data
    return None, data

def create_version_snapshot(frame, preserve_image=False):
    """Create a snapshot of the current frame state for version history."""
    import shutil

    viz = frame.get('visualization', {})
    version_num = frame.get('currentVersion', 1)
    frame_id = frame.get('id', 0)

    # Get current image path
    current_image_path = viz.get('imagePath')
    versioned_image_path = current_image_path

    # If we need to preserve the image, copy it to a versioned filename
    if preserve_image and current_image_path:
        # Build the full path to the original image
        # current_image_path is like "images/frame_001.png"
        original_file = Path(current_image_path)

        print(f"DEBUG: Trying to preserve image from: {original_file} (exists: {original_file.exists()})")
        print(f"DEBUG: Absolute path: {original_file.absolute()}")

        if original_file.exists():
            # Create versioned filename: frame_001_v1.png
            versioned_filename = f'frame_{frame_id:03d}_v{version_num}.png'
            versioned_file = IMAGES_DIR / versioned_filename

            print(f"DEBUG: Copying to: {versioned_file}")

            try:
                shutil.copy2(str(original_file), str(versioned_file))
                versioned_image_path = f'images/{versioned_filename}'
                print(f"SUCCESS: Preserved image as {versioned_image_path}")
            except Exception as e:
                print(f"ERROR: Could not preserve image: {e}")
                versioned_image_path = current_image_path
        else:
            print(f"WARNING: Original image not found at {original_file.absolute()}")

    return {
        'version': version_num,
        'timestamp': frame.get('timestamp', datetime.now().isoformat() + 'Z'),
        'title': viz.get('title', ''),
        'themes': viz.get('themes', []),
        'notes': viz.get('notes', ''),
        'imagePrompt': viz.get('imagePrompt', ''),
        'imagePath': versioned_image_path
    }

def save_version_history(frame, preserve_image=False):
    """Save current state to version history before making changes."""
    # Initialize version history if not exists
    if 'versionHistory' not in frame:
        frame['versionHistory'] = []
        frame['currentVersion'] = 1

    # Create snapshot of current state (preserve image if requested)
    snapshot = create_version_snapshot(frame, preserve_image=preserve_image)

    # Only save if there's actual content
    if snapshot['title'] or snapshot['themes'] or snapshot['notes'] or snapshot['imagePath']:
        # Check if this version already exists in history
        existing_versions = [v['version'] for v in frame['versionHistory']]
        if snapshot['version'] not in existing_versions:
            frame['versionHistory'].append(snapshot)

    # Increment version number for the new changes
    frame['currentVersion'] = frame.get('currentVersion', 1) + 1

def generate_default_prompt(reference, text):
    return f"Biblical scene depicting: {text}. Epic, cinematic, highly detailed, divine lighting, religious art style, 8k quality"

def get_frame_prompt(frame):
    viz = frame.get('visualization', {})
    if 'imagePrompt' in viz and viz['imagePrompt']:
        return viz['imagePrompt']
    return generate_default_prompt(frame['reference'], frame['text'])

# ============================================================================
# IMAGE GENERATION
# ============================================================================

def upload_to_cloudinary(image_data, public_id):
    """Upload image data to Cloudinary and return the URL."""
    try:
        result = cloudinary.uploader.upload(
            image_data,
            public_id=public_id,
            folder='genesis-visualized',
            resource_type='image',
            overwrite=True
        )
        return result['secure_url']
    except Exception as e:
        print(f"Cloudinary upload error: {e}")
        return None

def regenerate_image(frame_id, prompt):
    """Generate image with DALL-E 3"""
    api_key = load_api_key()
    if not api_key:
        return {"success": False, "error": "No API key found in .env"}

    IMAGES_DIR.mkdir(exist_ok=True)

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'dall-e-3',
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024',
        'quality': 'hd',
        'style': 'vivid'
    }

    try:
        print(f"Generating image for frame {frame_id}...")
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data,
            timeout=120
        )

        if response.status_code != 200:
            return {"success": False, "error": f"API error: {response.status_code}"}

        result = response.json()
        image_url = result['data'][0]['url']

        # Download image from DALL-E
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code != 200:
            return {"success": False, "error": "Failed to download image from DALL-E"}

        image_data = img_response.content
        image_filename = f'frame_{frame_id:03d}.png'

        # Upload to Cloudinary if enabled
        if USE_CLOUD_STORAGE:
            print(f"Uploading to Cloudinary...")
            cloudinary_url = upload_to_cloudinary(image_data, f'frame_{frame_id:03d}')
            if cloudinary_url:
                print(f"Image uploaded to Cloudinary: {cloudinary_url}")
                return {"success": True, "imagePath": cloudinary_url}
            else:
                print("Cloudinary upload failed, falling back to local storage")

        # Save locally (fallback or local-only mode)
        image_path = IMAGES_DIR / image_filename
        with open(image_path, 'wb') as f:
            f.write(image_data)

        print(f"Image saved locally: {image_path}")
        return {"success": True, "imagePath": f'images/{image_filename}'}

    except Exception as e:
        return {"success": False, "error": str(e)}

def regenerate_ascii(frame_id, reference, verse_text):
    """Generate ASCII art with GPT-4"""
    api_key = load_api_key()
    if not api_key:
        return {"success": False, "error": "No API key found in .env"}

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    prompt = f"""Create ASCII art for this Bible verse. The art should be creative, meaningful, and visually represent the scene or concept described.

Verse: {reference}
"{verse_text}"

Requirements:
- Use standard ASCII characters only (letters, numbers, symbols like / \\ | _ - = + * # @ etc.)
- Art should be approximately 40-60 characters wide and 15-25 lines tall
- Include meaningful visual elements that represent the verse
- You may include the verse reference as a decorative header
- Make it artistic and evocative of the biblical scene
- Use box-drawing characters if appropriate (like ╔ ╗ ╚ ╝ ║ ═)

Return ONLY the ASCII art, no explanations or additional text."""

    data = {
        'model': 'gpt-4',
        'messages': [
            {
                'role': 'system',
                'content': 'You are an ASCII art creator specializing in biblical scenes. Create beautiful, meaningful ASCII art that visually represents Bible verses. Return only the ASCII art itself, no explanations.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        'max_tokens': 1000,
        'temperature': 0.8
    }

    try:
        print(f"Generating ASCII art for frame {frame_id}...")
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:
            return {"success": False, "error": f"API error: {response.status_code}"}

        result = response.json()
        ascii_art = result['choices'][0]['message']['content'].strip()

        print(f"ASCII art generated for frame {frame_id}")
        return {"success": True, "asciiArt": ascii_art}

    except Exception as e:
        return {"success": False, "error": str(e)}

def fix_ascii_borders(ascii_art):
    """
    Precisely fix ASCII art borders so all edges align perfectly.
    This handles emoji width issues and ensures consistent line widths.
    """
    import unicodedata

    def char_width(char):
        """Get the display width of a character (1 or 2 for wide chars/emojis)"""
        if ord(char) > 0x1F300:  # Emojis and symbols
            return 2
        # Check East Asian Width
        ea = unicodedata.east_asian_width(char)
        if ea in ('F', 'W'):  # Fullwidth or Wide
            return 2
        return 1

    def visual_width(s):
        """Calculate the visual display width of a string"""
        return sum(char_width(c) for c in s)

    def pad_to_width(s, target_width):
        """Pad a string with spaces to reach target visual width"""
        current = visual_width(s)
        if current < target_width:
            return s + ' ' * (target_width - current)
        return s

    lines = ascii_art.split('\n')

    # Remove empty lines at start/end
    while lines and lines[0].strip() == '':
        lines.pop(0)
    while lines and lines[-1].strip() == '':
        lines.pop()

    if not lines:
        return ascii_art

    # Detect if this has box borders
    has_top_border = lines[0].strip().startswith('╔') and lines[0].strip().endswith('╗')
    has_bottom_border = lines[-1].strip().startswith('╚') and lines[-1].strip().endswith('╝')

    if has_top_border and has_bottom_border:
        # This is a boxed ASCII art - fix the borders precisely

        # Find the intended width from the top border
        top_line = lines[0].strip()
        # Count the ═ characters between ╔ and ╗
        inner_width = top_line.count('═')
        total_width = inner_width + 2  # +2 for ╔ and ╗

        fixed_lines = []

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Top border
            if stripped.startswith('╔') and stripped.endswith('╗'):
                fixed_lines.append('╔' + '═' * inner_width + '╗')

            # Bottom border
            elif stripped.startswith('╚') and stripped.endswith('╝'):
                fixed_lines.append('╚' + '═' * inner_width + '╝')

            # Divider line
            elif stripped.startswith('╠') and stripped.endswith('╣'):
                fixed_lines.append('╠' + '═' * inner_width + '╣')

            # Content line with side borders
            elif stripped.startswith('║') and '║' in stripped[1:]:
                # Extract content between the borders
                content = stripped[1:]  # Remove left ║
                # Find the last ║
                last_border = content.rfind('║')
                if last_border > 0:
                    content = content[:last_border]  # Remove right ║ and anything after
                else:
                    content = content.rstrip('║')

                # Calculate how much padding we need
                content_visual_width = visual_width(content)
                needed_width = inner_width

                if content_visual_width < needed_width:
                    # Pad the content to fit
                    padding = needed_width - content_visual_width
                    content = content + ' ' * padding
                elif content_visual_width > needed_width:
                    # Content too wide - try to trim trailing spaces
                    content = content.rstrip()
                    content_visual_width = visual_width(content)
                    if content_visual_width < needed_width:
                        padding = needed_width - content_visual_width
                        content = content + ' ' * padding

                fixed_lines.append('║' + content + '║')

            # Line without proper borders - try to add them
            elif stripped and not stripped.startswith('║'):
                content = stripped
                content_visual_width = visual_width(content)
                if content_visual_width < inner_width:
                    # Center the content
                    total_padding = inner_width - content_visual_width
                    left_pad = total_padding // 2
                    right_pad = total_padding - left_pad
                    content = ' ' * left_pad + content + ' ' * right_pad
                fixed_lines.append('║' + content + '║')

            else:
                # Empty or unrecognized - make empty bordered line
                fixed_lines.append('║' + ' ' * inner_width + '║')

        return '\n'.join(fixed_lines)

    else:
        # No box borders - just ensure consistent width
        max_width = max(visual_width(line.rstrip()) for line in lines)
        fixed_lines = []
        for line in lines:
            stripped = line.rstrip()
            current_width = visual_width(stripped)
            if current_width < max_width:
                stripped = stripped + ' ' * (max_width - current_width)
            fixed_lines.append(stripped)
        return '\n'.join(fixed_lines)

def format_ascii_with_claude(frame_id, reference, verse_text, current_ascii):
    """Use Claude to intelligently analyze and recreate ASCII art based on verse content"""
    api_key = load_env_var('ANTHROPIC_API_KEY')
    if not api_key:
        return {"success": False, "error": "No ANTHROPIC_API_KEY found in .env. Please add your Anthropic API key."}

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json',
        'anthropic-version': '2023-06-01'
    }

    # Calculate the width of the original art
    lines = current_ascii.split('\n')
    max_width = max(len(line) for line in lines) if lines else 60
    target_width = max(max_width, 56)  # At least 56 chars wide

    system_prompt = """You are a master ASCII art craftsman dedicated to creating beautiful, perfectly formatted ASCII art for a Bible visualization project. This is sacred work - every detail matters.

Your expertise includes:
- Perfect alignment of box-drawing characters
- Symmetrical, balanced compositions
- Clean, professional presentation
- Preserving the spiritual meaning and artistic intent

You take great pride in your work and never produce sloppy output."""

    user_prompt = f"""SACRED TASK: Restore and perfect this ASCII art for {reference}

THE VERSE: "{verse_text}"

CURRENT ASCII ART (needs fixing):
{current_ascii}

═══════════════════════════════════════════════════════════

REQUIREMENTS FOR PERFECTION:

1. EXACT WIDTH: Every single line must be EXACTLY {target_width} characters wide.
   - Pad shorter lines with spaces on the right
   - Do not exceed {target_width} characters on any line

2. BOX BORDERS (if present):
   ╔{'═' * (target_width-2)}╗  <- Top border
   ║{' ' * (target_width-2)}║  <- Side borders with content
   ╚{'═' * (target_width-2)}╝  <- Bottom border

3. CENTERING:
   - The verse reference should be centered in the header
   - All text content should be visually centered
   - Decorative elements should be symmetrical

4. PRESERVE:
   - Keep the original artistic vision and symbols
   - Keep any emojis (📖 ✨ 🌟 👑 etc.)
   - Keep figures, scenes, and decorative elements

5. PROFESSIONAL QUALITY:
   - No broken or misaligned borders
   - No jagged edges
   - Clean, crisp appearance
   - Worthy of displaying God's Word

OUTPUT: Return ONLY the perfected ASCII art. No explanations, no markdown, no code blocks. Just the pure ASCII art ready for display."""

    data = {
        'model': 'claude-sonnet-4-20250514',
        'max_tokens': 2500,
        'temperature': 0.2,
        'system': system_prompt,
        'messages': [
            {
                'role': 'user',
                'content': user_prompt
            }
        ]
    }

    try:
        print(f"Formatting ASCII art with Claude for frame {frame_id}...")
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:
            error_detail = response.text
            print(f"Anthropic API error: {response.status_code} - {error_detail}")
            return {"success": False, "error": f"API error: {response.status_code}"}

        result = response.json()
        ascii_art = result['content'][0]['text'].strip()

        # Remove any markdown code block formatting if present
        if ascii_art.startswith('```'):
            lines = ascii_art.split('\n')
            # Remove first and last line if they're code block markers
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            ascii_art = '\n'.join(lines)

        # POST-PROCESSING: Use our precise border fixing algorithm
        ascii_art = fix_ascii_borders(ascii_art)

        print(f"ASCII art formatted with Claude for frame {frame_id}")
        return {"success": True, "asciiArt": ascii_art}

    except Exception as e:
        print(f"Error formatting ASCII with Claude: {e}")
        return {"success": False, "error": str(e)}

# ============================================================================
# API HANDLER
# ============================================================================

class APIHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # API: Get frame data
        if path.startswith('/api/frame/') and '/versions' not in path:
            try:
                frame_id = int(path.split('/')[-1])
                frame, _ = get_frame_by_id(frame_id)
                if frame:
                    # Add prompt and version info to response
                    response = {
                        "id": frame['id'],
                        "reference": frame['reference'],
                        "text": frame['text'],
                        "title": frame['visualization'].get('title', ''),
                        "asciiArt": frame['visualization'].get('asciiArt', ''),
                        "imagePrompt": get_frame_prompt(frame),
                        "imagePath": frame['visualization'].get('imagePath'),
                        "currentVersion": frame.get('currentVersion', 1),
                        "versionCount": len(frame.get('versionHistory', [])) + 1
                    }
                    self.send_json(response)
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except:
                self.send_json({"error": "Invalid frame ID"}, 400)
            return

        # API: Get version history for a frame
        if '/versions' in path:
            try:
                frame_id = int(path.split('/')[3])
                frame, _ = get_frame_by_id(frame_id)
                if frame:
                    # Build versions list including current
                    versions = []

                    # Add historical versions
                    for v in frame.get('versionHistory', []):
                        versions.append({
                            'version': v['version'],
                            'timestamp': v['timestamp'],
                            'title': v.get('title', ''),
                            'hasImage': bool(v.get('imagePath')),
                            'imagePath': v.get('imagePath'),
                            'asciiArt': v.get('asciiArt', ''),
                            'isCurrent': False
                        })

                    # Add current version
                    viz = frame.get('visualization', {})
                    versions.append({
                        'version': frame.get('currentVersion', 1),
                        'timestamp': frame.get('timestamp', ''),
                        'title': viz.get('title', ''),
                        'hasImage': bool(viz.get('imagePath')),
                        'imagePath': viz.get('imagePath'),
                        'asciiArt': viz.get('asciiArt', ''),
                        'isCurrent': True
                    })

                    # Sort by version number
                    versions.sort(key=lambda x: x['version'])

                    self.send_json({
                        "frameId": frame['id'],
                        "reference": frame['reference'],
                        "versions": versions
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 400)
            return

        # API: Get current user session
        if path == '/api/auth/me':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            session = auth.verify_session(token)
            if session:
                self.send_json({
                    "authenticated": True,
                    "username": session['username'],
                    "role": session['role']
                })
            else:
                self.send_json({"authenticated": False}, 401)
            return

        # API: Get all users (admin only)
        if path == '/api/auth/users':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            session = auth.verify_session(token)
            if session and session['role'] == 'admin':
                self.send_json({"users": auth.get_all_users()})
            else:
                self.send_json({"error": "Admin access required"}, 403)
            return

        # Serve static files
        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        # Read request body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            post_data = json.loads(body) if body else {}
        except:
            post_data = {}

        # ====================================================================
        # AUTHENTICATION ENDPOINTS
        # ====================================================================

        # API: Login
        if path == '/api/auth/login':
            username = post_data.get('username', '')
            password = post_data.get('password', '')
            if not username or not password:
                self.send_json({"error": "Username and password required"}, 400)
                return
            result = auth.login(username, password)
            self.send_json(result, 200 if result['success'] else 401)
            return

        # API: Logout
        if path == '/api/auth/logout':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            result = auth.logout(token)
            self.send_json(result)
            return

        # API: Register new user (admin only)
        if path == '/api/auth/register':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            session = auth.verify_session(token)
            if not session or session['role'] != 'admin':
                self.send_json({"error": "Admin access required"}, 403)
                return

            username = post_data.get('username', '')
            password = post_data.get('password', '')
            role = post_data.get('role', 'editor')

            if not username or not password:
                self.send_json({"error": "Username and password required"}, 400)
                return

            result = auth.create_user(username, password, role)
            self.send_json(result, 200 if result['success'] else 400)
            return

        # API: Delete user (admin only)
        if path == '/api/auth/delete':
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            username = post_data.get('username', '')
            result = auth.delete_user(username, token)
            self.send_json(result, 200 if result['success'] else 403)
            return

        # API: Change password
        if path == '/api/auth/password':
            username = post_data.get('username', '')
            old_password = post_data.get('oldPassword', '')
            new_password = post_data.get('newPassword', '')
            result = auth.change_password(username, old_password, new_password)
            self.send_json(result, 200 if result['success'] else 400)
            return

        # ====================================================================
        # FRAME EDITING ENDPOINTS (require authentication)
        # ====================================================================

        # Helper to check authentication for editing
        def require_auth():
            token = self.headers.get('Authorization', '').replace('Bearer ', '')
            session = auth.verify_session(token)
            if not session:
                self.send_json({"error": "Authentication required"}, 401)
                return None
            return session

        # API: Save all changes (with version history)
        if path.startswith('/api/frame/') and path.endswith('/save'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Save current state to version history BEFORE making changes
                    save_version_history(frame)

                    # Update with new values
                    frame['visualization']['title'] = post_data.get('title', frame['visualization'].get('title', ''))
                    frame['visualization']['themes'] = post_data.get('themes', frame['visualization'].get('themes', []))
                    frame['visualization']['notes'] = post_data.get('notes', frame['visualization'].get('notes', ''))
                    frame['visualization']['imagePrompt'] = post_data.get('imagePrompt', '')
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'

                    save_database(data)
                    self.send_json({
                        "success": True,
                        "currentVersion": frame['currentVersion'],
                        "versionCount": len(frame.get('versionHistory', [])) + 1
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Update ASCII art (legacy - no version history)
        if path.startswith('/api/frame/') and path.endswith('/ascii'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    frame['visualization']['asciiArt'] = post_data.get('asciiArt', '')
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'
                    save_database(data)
                    self.send_json({"success": True})
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Update prompt (legacy - no version history)
        if path.startswith('/api/frame/') and path.endswith('/prompt'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    frame['visualization']['imagePrompt'] = post_data.get('imagePrompt', '')
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'
                    save_database(data)
                    self.send_json({"success": True})
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Update title (legacy - no version history)
        if path.startswith('/api/frame/') and path.endswith('/title'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    frame['visualization']['title'] = post_data.get('title', '')
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'
                    save_database(data)
                    self.send_json({"success": True})
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Regenerate image (with version history)
        if path.startswith('/api/frame/') and path.endswith('/regenerate'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Save current state to version history BEFORE regenerating
                    # preserve_image=True copies the current image to a versioned filename
                    save_version_history(frame, preserve_image=True)

                    prompt = post_data.get('imagePrompt', get_frame_prompt(frame))

                    # Save prompt
                    frame['visualization']['imagePrompt'] = prompt

                    # Generate image
                    result = regenerate_image(frame_id, prompt)

                    if result['success']:
                        frame['visualization']['imagePath'] = result['imagePath']
                        frame['timestamp'] = datetime.now().isoformat() + 'Z'
                        save_database(data)
                        self.send_json({
                            "success": True,
                            "imagePath": result['imagePath'],
                            "currentVersion": frame['currentVersion']
                        })
                    else:
                        save_database(data)  # Still save the prompt
                        self.send_json(result, 500)
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Regenerate ASCII art
        if path.startswith('/api/frame/') and path.endswith('/regenerate-ascii'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Generate new ASCII art
                    result = regenerate_ascii(frame_id, frame['reference'], frame['text'])

                    if result['success']:
                        self.send_json({
                            "success": True,
                            "asciiArt": result['asciiArt']
                        })
                    else:
                        self.send_json(result, 500)
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Format ASCII art with Claude (intelligent formatting)
        if path.startswith('/api/frame/') and path.endswith('/format-ascii'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    current_ascii = frame['visualization'].get('asciiArt', '')
                    # Use Claude to intelligently format/recreate the ASCII
                    result = format_ascii_with_claude(
                        frame_id,
                        frame['reference'],
                        frame['text'],
                        current_ascii
                    )

                    if result['success']:
                        self.send_json({
                            "success": True,
                            "asciiArt": result['asciiArt']
                        })
                    else:
                        self.send_json(result, 500)
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Quick fix borders (local, no AI - instant)
        if path.startswith('/api/frame/') and path.endswith('/fix-borders'):
            try:
                frame_id = int(path.split('/')[3])
                frame, data = get_frame_by_id(frame_id)
                if frame:
                    current_ascii = frame['visualization'].get('asciiArt', '')
                    # Use our precise local border fixing algorithm
                    fixed_ascii = fix_ascii_borders(current_ascii)
                    self.send_json({
                        "success": True,
                        "asciiArt": fixed_ascii
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Restore a specific version
        if path.startswith('/api/frame/') and path.endswith('/restore'):
            try:
                frame_id = int(path.split('/')[3])
                version_to_restore = post_data.get('version')

                if version_to_restore is None:
                    self.send_json({"error": "Version number required"}, 400)
                    return

                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Find the version in history
                    version_data = None
                    for v in frame.get('versionHistory', []):
                        if v['version'] == version_to_restore:
                            version_data = v
                            break

                    if not version_data:
                        self.send_json({"error": f"Version {version_to_restore} not found"}, 404)
                        return

                    # Save current state to history before restoring
                    save_version_history(frame)

                    # Restore the old version
                    frame['visualization']['title'] = version_data.get('title', '')
                    frame['visualization']['themes'] = version_data.get('themes', [])
                    frame['visualization']['notes'] = version_data.get('notes', '')
                    frame['visualization']['imagePrompt'] = version_data.get('imagePrompt', '')
                    frame['visualization']['imagePath'] = version_data.get('imagePath')
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'

                    save_database(data)
                    self.send_json({
                        "success": True,
                        "restoredVersion": version_to_restore,
                        "currentVersion": frame['currentVersion']
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Use ASCII from a specific version
        if path.startswith('/api/frame/') and path.endswith('/use-ascii'):
            try:
                frame_id = int(path.split('/')[3])
                version_to_use = post_data.get('version')

                if version_to_use is None:
                    self.send_json({"error": "Version number required"}, 400)
                    return

                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Find the version in history
                    version_data = None
                    for v in frame.get('versionHistory', []):
                        if v['version'] == version_to_use:
                            version_data = v
                            break

                    if not version_data:
                        self.send_json({"error": f"Version {version_to_use} not found"}, 404)
                        return

                    if not version_data.get('asciiArt'):
                        self.send_json({"error": f"Version {version_to_use} has no ASCII art"}, 400)
                        return

                    # Save current state first
                    save_version_history(frame, preserve_image=True)

                    # Apply only the ASCII from that version
                    frame['visualization']['asciiArt'] = version_data['asciiArt']
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'

                    save_database(data)
                    self.send_json({
                        "success": True,
                        "asciiArt": version_data['asciiArt'],
                        "currentVersion": frame['currentVersion']
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: Use image from a specific version
        if path.startswith('/api/frame/') and path.endswith('/use-image'):
            try:
                frame_id = int(path.split('/')[3])
                version_to_use = post_data.get('version')

                if version_to_use is None:
                    self.send_json({"error": "Version number required"}, 400)
                    return

                frame, data = get_frame_by_id(frame_id)
                if frame:
                    # Find the version in history
                    version_data = None
                    for v in frame.get('versionHistory', []):
                        if v['version'] == version_to_use:
                            version_data = v
                            break

                    if not version_data:
                        self.send_json({"error": f"Version {version_to_use} not found"}, 404)
                        return

                    if not version_data.get('imagePath'):
                        self.send_json({"error": f"Version {version_to_use} has no image"}, 400)
                        return

                    # Save current state first
                    save_version_history(frame, preserve_image=True)

                    # Apply only the image from that version
                    frame['visualization']['imagePath'] = version_data['imagePath']
                    frame['timestamp'] = datetime.now().isoformat() + 'Z'

                    save_database(data)
                    self.send_json({
                        "success": True,
                        "imagePath": version_data['imagePath'],
                        "currentVersion": frame['currentVersion']
                    })
                else:
                    self.send_json({"error": "Frame not found"}, 404)
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        self.send_json({"error": "Unknown endpoint"}, 404)

    def log_message(self, format, *args):
        print(f"[API] {args[0]}")

# ============================================================================
# MAIN
# ============================================================================

def run_api_server():
    server = HTTPServer(('localhost', API_PORT), APIHandler)
    print(f"API server running on http://localhost:{API_PORT}")
    server.serve_forever()

def run_static_server():
    os.chdir(Path(__file__).parent)
    handler = SimpleHTTPRequestHandler
    server = HTTPServer(('localhost', STATIC_PORT), handler)
    print(f"Static server running on http://localhost:{STATIC_PORT}")
    server.serve_forever()

if __name__ == "__main__":
    print("=" * 60)
    print("Genesis Frame Editor - Web Server")
    print("=" * 60)

    # Run both servers in threads
    api_thread = threading.Thread(target=run_api_server, daemon=True)
    static_thread = threading.Thread(target=run_static_server, daemon=True)

    api_thread.start()
    static_thread.start()

    print(f"\nVisualizer: http://localhost:{STATIC_PORT}/visualizer.html")
    print(f"API: http://localhost:{API_PORT}/api/frame/1")
    print("\nPress Ctrl+C to stop...\n")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nShutting down...")
