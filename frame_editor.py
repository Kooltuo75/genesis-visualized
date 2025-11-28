"""
Genesis Frame Editor - Unified Quality Control Tool
====================================================

A comprehensive tool for viewing, editing, and quality-checking
all frames in the Genesis Bible Visualizer project.

Usage:
    python frame_editor.py              # Start at frame 1
    python frame_editor.py <frame_id>   # Start at specific frame
    python frame_editor.py "Genesis 5:1" # Start at specific verse

Features:
    - Navigate through all 592 frames
    - View verse text, ASCII art, image prompt, and HD image status
    - Edit any field with automatic Notepad integration
    - Regenerate HD images with DALL-E 3
    - Track changes and save when ready
    - Search and jump to any frame
"""

import json
import sys
import os
import subprocess
import tempfile
import requests
from datetime import datetime
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

DATABASE_FILE = "frames-database.json"
IMAGES_DIR = Path("images")

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def load_database():
    """Load the frames database."""
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data):
    """Save the frames database."""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return True

def load_api_key():
    """Load OpenAI API key from .env file."""
    env_path = Path('.env')
    if not env_path.exists():
        return None
    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                return line.strip().split('=', 1)[1]
    return None

# ============================================================================
# EDITOR CLASS
# ============================================================================

class FrameEditor:
    def __init__(self, start_frame=1):
        self.data = load_database()
        self.frames = self.data['frames']
        self.current_index = 0
        self.unsaved_changes = False
        self.modified_fields = set()

        # Find starting frame
        if isinstance(start_frame, int):
            self.current_index = max(0, min(start_frame - 1, len(self.frames) - 1))
        else:
            # Search by reference
            for i, f in enumerate(self.frames):
                if f['reference'].lower() == start_frame.lower():
                    self.current_index = i
                    break

    @property
    def current_frame(self):
        return self.frames[self.current_index]

    @property
    def total_frames(self):
        return len(self.frames)

    def get_prompt(self, frame):
        """Get the image prompt for a frame."""
        viz = frame.get('visualization', {})
        if 'imagePrompt' in viz and viz['imagePrompt']:
            return viz['imagePrompt']
        # Generate default
        return f"Biblical scene depicting: {frame['text']}. Epic, cinematic, highly detailed, divine lighting, religious art style, 8k quality"

    def get_image_status(self, frame):
        """Check if HD image exists."""
        img_path = frame.get('visualization', {}).get('imagePath')
        if not img_path:
            return "MISSING", None
        if os.path.exists(img_path):
            size = os.path.getsize(img_path)
            return "OK", f"{img_path} ({size/1024/1024:.1f} MB)"
        return "FILE NOT FOUND", img_path

    # ------------------------------------------------------------------------
    # DISPLAY
    # ------------------------------------------------------------------------

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_frame(self):
        """Display the current frame with all details."""
        self.clear_screen()
        frame = self.current_frame
        viz = frame.get('visualization', {})

        # Header
        print("=" * 80)
        print(f"  GENESIS FRAME EDITOR  |  Frame {frame['id']} of {self.total_frames}  |  {frame['reference']}")
        if self.unsaved_changes:
            print(f"  ** UNSAVED CHANGES: {', '.join(self.modified_fields)} **")
        print("=" * 80)

        # Verse Info
        print(f"\n[TITLE] {viz.get('title', 'N/A')}")
        print(f"\n[VERSE TEXT]")
        print(f"  \"{frame['text']}\"")

        # Image Status
        status, details = self.get_image_status(frame)
        status_icon = "OK" if status == "OK" else "!!"
        print(f"\n[HD IMAGE] [{status_icon}] {status}")
        if details:
            print(f"  {details}")

        # Image Prompt (truncated)
        prompt = self.get_prompt(frame)
        print(f"\n[IMAGE PROMPT]")
        if len(prompt) > 150:
            print(f"  {prompt[:150]}...")
        else:
            print(f"  {prompt}")

        # ASCII Art (show first 15 lines)
        ascii_art = viz.get('asciiArt', '')
        print(f"\n[ASCII ART]")
        print("-" * 60)
        lines = ascii_art.split('\n')
        for line in lines[:15]:
            print(f"  {line}")
        if len(lines) > 15:
            print(f"  ... ({len(lines) - 15} more lines)")
        print("-" * 60)

        # Menu
        print("\n" + "=" * 80)
        print("  NAVIGATION:  [N]ext  [P]rev  [J]ump  [S]earch  [G]o to frame")
        print("  EDIT:        [1]Title  [2]ASCII Art  [3]Prompt  [4]Regenerate Image")
        print("  ACTIONS:     [V]iew Full ASCII  [O]pen Image  [W]Save  [Q]uit")
        print("=" * 80)

    def display_full_ascii(self):
        """Display full ASCII art."""
        self.clear_screen()
        frame = self.current_frame
        viz = frame.get('visualization', {})

        print("=" * 80)
        print(f"  ASCII ART - Frame {frame['id']}: {frame['reference']}")
        print("=" * 80)
        print(viz.get('asciiArt', '(No ASCII art)'))
        print("=" * 80)
        input("\nPress Enter to return...")

    def display_full_prompt(self):
        """Display full image prompt."""
        self.clear_screen()
        frame = self.current_frame

        print("=" * 80)
        print(f"  IMAGE PROMPT - Frame {frame['id']}: {frame['reference']}")
        print("=" * 80)
        print(self.get_prompt(frame))
        print("=" * 80)
        input("\nPress Enter to return...")

    # ------------------------------------------------------------------------
    # NAVIGATION
    # ------------------------------------------------------------------------

    def next_frame(self):
        if self.current_index < len(self.frames) - 1:
            self.current_index += 1
            return True
        return False

    def prev_frame(self):
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False

    def jump_to_frame(self, frame_id):
        """Jump to a specific frame by ID."""
        try:
            fid = int(frame_id)
            if 1 <= fid <= len(self.frames):
                self.current_index = fid - 1
                return True
        except ValueError:
            pass
        return False

    def search_frames(self, query):
        """Search frames by keyword. Returns list of matches."""
        query_lower = query.lower()
        matches = []
        for i, frame in enumerate(self.frames):
            if (query_lower in frame['text'].lower() or
                query_lower in frame['reference'].lower() or
                query_lower in frame.get('visualization', {}).get('title', '').lower() or
                query_lower in frame.get('visualization', {}).get('asciiArt', '').lower()):
                matches.append((i, frame))
        return matches

    # ------------------------------------------------------------------------
    # EDITING
    # ------------------------------------------------------------------------

    def open_in_editor(self, content, title="Edit"):
        """Open content in Notepad for editing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = f.name

        try:
            print(f"\nOpening {title} in Notepad...")
            print("Edit, save (Ctrl+S), and close Notepad to continue.")
            subprocess.run(['notepad.exe', temp_path], check=True)

            with open(temp_path, 'r', encoding='utf-8') as f:
                return f.read()
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass

    def edit_title(self):
        """Edit the frame title."""
        frame = self.current_frame
        current = frame.get('visualization', {}).get('title', '')

        new_title = self.open_in_editor(current, "Title")
        new_title = new_title.strip()

        if new_title and new_title != current:
            frame['visualization']['title'] = new_title
            self.unsaved_changes = True
            self.modified_fields.add('title')
            print(f"\nTitle updated!")
        else:
            print("\nNo changes made.")
        input("Press Enter to continue...")

    def edit_ascii_art(self):
        """Edit the ASCII art."""
        frame = self.current_frame
        current = frame.get('visualization', {}).get('asciiArt', '')

        new_ascii = self.open_in_editor(current, "ASCII Art")

        if new_ascii != current:
            frame['visualization']['asciiArt'] = new_ascii
            self.unsaved_changes = True
            self.modified_fields.add('asciiArt')
            print(f"\nASCII art updated!")
        else:
            print("\nNo changes made.")
        input("Press Enter to continue...")

    def edit_prompt(self):
        """Edit the image prompt."""
        frame = self.current_frame
        current = self.get_prompt(frame)

        new_prompt = self.open_in_editor(current, "Image Prompt")
        new_prompt = new_prompt.strip()

        if new_prompt and new_prompt != current:
            frame['visualization']['imagePrompt'] = new_prompt
            self.unsaved_changes = True
            self.modified_fields.add('imagePrompt')
            print(f"\nImage prompt updated!")

            regen = input("Regenerate image with new prompt? (y/n): ").strip().lower()
            if regen == 'y':
                self.regenerate_image()
                return
        else:
            print("\nNo changes made.")
        input("Press Enter to continue...")

    def regenerate_image(self):
        """Regenerate the HD image using DALL-E 3."""
        frame = self.current_frame
        prompt = self.get_prompt(frame)

        print(f"\nRegenerating image for Frame {frame['id']}...")
        print(f"Prompt: {prompt[:80]}...")

        api_key = load_api_key()
        if not api_key:
            print("\nERROR: No API key found in .env file")
            input("Press Enter to continue...")
            return

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
            print("\nCalling DALL-E 3 API...")
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=data,
                timeout=120
            )

            if response.status_code != 200:
                print(f"\nERROR: API returned {response.status_code}")
                print(response.text[:200])
                input("Press Enter to continue...")
                return

            result = response.json()
            image_url = result['data'][0]['url']

            print("Downloading image...")
            img_response = requests.get(image_url, timeout=30)

            if img_response.status_code == 200:
                image_filename = f'frame_{frame["id"]:03d}.png'
                image_path = IMAGES_DIR / image_filename

                with open(image_path, 'wb') as f:
                    f.write(img_response.content)

                frame['visualization']['imagePath'] = f'images/{image_filename}'
                frame['visualization']['imagePrompt'] = prompt
                self.unsaved_changes = True
                self.modified_fields.add('imagePath')

                print(f"\nSUCCESS! Image saved: {image_path}")
            else:
                print(f"\nERROR: Failed to download image")

        except Exception as e:
            print(f"\nERROR: {e}")

        input("Press Enter to continue...")

    def open_image(self):
        """Open the HD image in default viewer."""
        frame = self.current_frame
        img_path = frame.get('visualization', {}).get('imagePath')

        if img_path and os.path.exists(img_path):
            print(f"\nOpening {img_path}...")
            os.startfile(img_path)
        else:
            print("\nNo image available for this frame.")
        input("Press Enter to continue...")

    # ------------------------------------------------------------------------
    # SAVE
    # ------------------------------------------------------------------------

    def save_changes(self):
        """Save all changes to database."""
        if not self.unsaved_changes:
            print("\nNo changes to save.")
            input("Press Enter to continue...")
            return

        # Update timestamp
        self.current_frame['timestamp'] = datetime.now().isoformat() + 'Z'

        # Update totals
        self.data['totalFrames'] = len(self.frames)
        self.data['currentFrameIndex'] = self.current_index

        save_database(self.data)

        print(f"\nChanges saved!")
        print(f"  Modified: {', '.join(self.modified_fields)}")
        self.unsaved_changes = False
        self.modified_fields.clear()
        input("Press Enter to continue...")

    # ------------------------------------------------------------------------
    # SEARCH UI
    # ------------------------------------------------------------------------

    def search_ui(self):
        """Interactive search interface."""
        self.clear_screen()
        print("=" * 80)
        print("  SEARCH FRAMES")
        print("=" * 80)

        query = input("\nEnter search term (or blank to cancel): ").strip()
        if not query:
            return

        matches = self.search_frames(query)

        if not matches:
            print(f"\nNo frames found matching '{query}'")
            input("Press Enter to continue...")
            return

        print(f"\nFound {len(matches)} matches:\n")

        # Show up to 20 matches
        for i, (idx, frame) in enumerate(matches[:20]):
            print(f"  {i+1:2}. Frame {frame['id']:3} | {frame['reference']:<15} | {frame['visualization'].get('title', '')[:40]}")

        if len(matches) > 20:
            print(f"\n  ... and {len(matches) - 20} more")

        print()
        choice = input("Enter number to jump to (or blank to cancel): ").strip()

        try:
            num = int(choice)
            if 1 <= num <= min(20, len(matches)):
                self.current_index = matches[num - 1][0]
        except ValueError:
            pass

    def jump_ui(self):
        """Jump to frame interface."""
        frame_id = input("\nEnter frame ID (1-592) or verse reference: ").strip()

        if not frame_id:
            return

        # Try as number first
        if self.jump_to_frame(frame_id):
            return

        # Try as reference
        for i, f in enumerate(self.frames):
            if f['reference'].lower() == frame_id.lower():
                self.current_index = i
                return

        print(f"Frame not found: {frame_id}")
        input("Press Enter to continue...")

    # ------------------------------------------------------------------------
    # MAIN LOOP
    # ------------------------------------------------------------------------

    def confirm_quit(self):
        """Confirm quit if there are unsaved changes."""
        if self.unsaved_changes:
            print(f"\nYou have unsaved changes: {', '.join(self.modified_fields)}")
            choice = input("Save before quitting? (y/n/cancel): ").strip().lower()
            if choice == 'cancel':
                return False
            if choice == 'y':
                self.save_changes()
        return True

    def run(self):
        """Main editor loop."""
        while True:
            self.display_frame()

            cmd = input("\nCommand: ").strip().upper()

            # Navigation
            if cmd == 'N':
                if not self.next_frame():
                    print("Already at last frame.")
                    input("Press Enter...")
            elif cmd == 'P':
                if not self.prev_frame():
                    print("Already at first frame.")
                    input("Press Enter...")
            elif cmd == 'J':
                self.jump_ui()
            elif cmd == 'S':
                self.search_ui()
            elif cmd == 'G':
                self.jump_ui()

            # Editing
            elif cmd == '1':
                self.edit_title()
            elif cmd == '2':
                self.edit_ascii_art()
            elif cmd == '3':
                self.edit_prompt()
            elif cmd == '4':
                self.regenerate_image()

            # Actions
            elif cmd == 'V':
                self.display_full_ascii()
            elif cmd == 'O':
                self.open_image()
            elif cmd == 'W':
                self.save_changes()
            elif cmd == 'Q':
                if self.confirm_quit():
                    print("\nGoodbye!")
                    break

            # Quick navigation with arrow-like keys
            elif cmd == '>' or cmd == '.':
                self.next_frame()
            elif cmd == '<' or cmd == ',':
                self.prev_frame()

# ============================================================================
# MAIN
# ============================================================================

def main():
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    # Parse starting frame
    start = 1
    if len(sys.argv) > 1:
        arg = ' '.join(sys.argv[1:])
        try:
            start = int(arg)
        except ValueError:
            start = arg  # Treat as verse reference

    print("Loading Genesis Frame Editor...")
    editor = FrameEditor(start)
    editor.run()

if __name__ == "__main__":
    main()
