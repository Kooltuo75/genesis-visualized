"""
ASCII Art Editor Tool
Edit the ASCII art of any frame in the Genesis Bible Visualizer

Usage:
    python edit_ascii.py <frame_id>
    python edit_ascii.py <verse_reference>

Examples:
    python edit_ascii.py 1
    python edit_ascii.py "Genesis 1:1"
    python edit_ascii.py 42
"""

import json
import sys
import os
import subprocess
import tempfile
from datetime import datetime

DATABASE_FILE = "frames-database.json"

def load_database():
    """Load the frames database."""
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(data):
    """Save the frames database."""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def find_frame(data, identifier):
    """Find a frame by ID or verse reference."""
    # Try as frame ID first
    try:
        frame_id = int(identifier)
        for frame in data['frames']:
            if frame['id'] == frame_id:
                return frame
        return None
    except ValueError:
        pass

    # Try as verse reference
    identifier_lower = identifier.lower().strip()
    for frame in data['frames']:
        if frame['reference'].lower() == identifier_lower:
            return frame

    return None

def open_in_editor(content):
    """Open content in a text editor and return the edited content."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name

    try:
        # Open in notepad (Windows) and wait for it to close
        print(f"\n📝 Opening ASCII art in Notepad...")
        print("   Edit the content, save (Ctrl+S), and close Notepad to continue.\n")

        # Use notepad on Windows
        subprocess.run(['notepad.exe', temp_path], check=True)

        # Read the edited content
        with open(temp_path, 'r', encoding='utf-8') as f:
            edited_content = f.read()

        return edited_content
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except:
            pass

def display_frame_info(frame):
    """Display frame information."""
    print("\n" + "="*60)
    print(f"Frame #{frame['id']}: {frame['reference']}")
    print("="*60)
    print(f"Title: {frame['visualization']['title']}")
    print(f"Verse: {frame['text'][:80]}..." if len(frame['text']) > 80 else f"Verse: {frame['text']}")
    print("-"*60)
    print("Current ASCII Art:")
    print("-"*60)
    print(frame['visualization']['asciiArt'])
    print("-"*60)

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable frames: 1-592")
        print("\nQuick search by chapter:")
        print("  Genesis 1: frames 1-31")
        print("  Genesis 2: frames 32-56")
        print("  Genesis 3: frames 57-80")
        print("  (etc.)")
        sys.exit(1)

    # Get the identifier (frame ID or verse reference)
    identifier = ' '.join(sys.argv[1:])

    # Load database
    print(f"Loading database...")
    data = load_database()

    # Find the frame
    frame = find_frame(data, identifier)

    if not frame:
        print(f"\n❌ Frame not found: {identifier}")
        print("\nTip: Use frame ID (1-592) or verse reference (e.g., 'Genesis 1:1')")
        sys.exit(1)

    # Display current frame info
    display_frame_info(frame)

    # Confirm edit
    response = input("\n✏️  Do you want to edit this ASCII art? (y/n): ").strip().lower()
    if response != 'y':
        print("Edit cancelled.")
        sys.exit(0)

    # Get current ASCII art
    original_ascii = frame['visualization']['asciiArt']

    # Open in editor
    edited_ascii = open_in_editor(original_ascii)

    # Check if changes were made
    if edited_ascii == original_ascii:
        print("\n⚠️  No changes detected. Database not updated.")
        sys.exit(0)

    # Show preview of changes
    print("\n" + "="*60)
    print("EDITED ASCII ART PREVIEW:")
    print("="*60)
    print(edited_ascii)
    print("="*60)

    # Confirm save
    response = input("\n💾 Save these changes to the database? (y/n): ").strip().lower()
    if response != 'y':
        print("Changes discarded.")
        sys.exit(0)

    # Update the frame
    frame['visualization']['asciiArt'] = edited_ascii
    frame['timestamp'] = datetime.now().isoformat() + 'Z'

    # Save database
    save_database(data)

    print(f"\n✅ Successfully updated ASCII art for Frame #{frame['id']} ({frame['reference']})")
    print(f"   Timestamp: {frame['timestamp']}")

if __name__ == "__main__":
    main()
