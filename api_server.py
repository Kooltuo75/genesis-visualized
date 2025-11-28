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
        'asciiArt': viz.get('asciiArt', ''),
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
    if snapshot['title'] or snapshot['asciiArt'] or snapshot['imagePath']:
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

# ============================================================================
# API HANDLER
# ============================================================================

class APIHandler(SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
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
                    frame['visualization']['asciiArt'] = post_data.get('asciiArt', frame['visualization'].get('asciiArt', ''))
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
                    frame['visualization']['asciiArt'] = version_data.get('asciiArt', '')
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
