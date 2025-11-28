"""
Image Prompt Editor Tool
View, edit, and regenerate HD images for Genesis Bible Visualizer frames

Usage:
    python edit_prompt.py <frame_id>
    python edit_prompt.py <verse_reference>

Examples:
    python edit_prompt.py 1
    python edit_prompt.py "Genesis 1:1"
    python edit_prompt.py 42
"""

import json
import sys
import os
import subprocess
import tempfile
import requests
from datetime import datetime
from pathlib import Path

DATABASE_FILE = "frames-database.json"

def load_api_key():
    """Load OpenAI API key from .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        print("ERROR: .env file not found. Please create one with your OPENAI_API_KEY")
        return None

    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                key = line.strip().split('=', 1)[1]
                return key

    print("ERROR: OPENAI_API_KEY not found in .env file")
    return None

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

def generate_default_prompt(reference, text):
    """Generate a default prompt from verse text."""
    # Some custom prompts for specific verses
    custom_prompts = {
        "Genesis 1:1": "Epic biblical scene of the creation of the universe, cosmic explosion of light and stars, heavens forming above with galaxies and nebulae, the earth taking shape below with swirling clouds and oceans, divine golden light radiating through space, majestic and awe-inspiring, ultra detailed, cinematic lighting, 8k quality, religious art style",
        "Genesis 1:2": "Dark primordial ocean covered in deep shadows, formless void and chaos, gentle dove-like spirit hovering above turbulent waters, mysterious deep waters stretching endlessly, darkness covering the surface, ethereal divine presence, moody atmospheric lighting, biblical epic scene, ultra detailed, 8k quality",
        "Genesis 1:3": "Brilliant burst of divine light piercing through absolute darkness, first rays of pure golden light illuminating the void, dramatic contrast between light and shadow, God's creation of light, cosmic spiritual scene, radiant beams spreading across space, epic biblical moment, cinematic lighting, 8k quality, religious masterpiece",
    }

    if reference in custom_prompts:
        return custom_prompts[reference]

    return f"Biblical scene depicting: {text}. Epic, cinematic, highly detailed, divine lighting, religious art style, 8k quality"

def get_frame_prompt(frame):
    """Get the prompt for a frame, generating default if not stored."""
    viz = frame.get('visualization', {})

    # Check if prompt is already stored
    if 'imagePrompt' in viz and viz['imagePrompt']:
        return viz['imagePrompt']

    # Generate default prompt
    return generate_default_prompt(frame['reference'], frame['text'])

def open_in_editor(content):
    """Open content in a text editor and return the edited content."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(content)
        temp_path = f.name

    try:
        print(f"\nOpening prompt in Notepad...")
        print("   Edit the prompt, save (Ctrl+S), and close Notepad to continue.\n")
        subprocess.run(['notepad.exe', temp_path], check=True)

        with open(temp_path, 'r', encoding='utf-8') as f:
            edited_content = f.read()

        return edited_content.strip()
    finally:
        try:
            os.unlink(temp_path)
        except:
            pass

def generate_image(prompt, frame_id):
    """Generate an image using DALL-E 3."""
    api_key = load_api_key()
    if not api_key:
        return None

    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    print(f"\nGenerating image with DALL-E 3...")
    print(f"   Prompt: {prompt[:80]}...")

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
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data,
            timeout=120
        )

        if response.status_code != 200:
            print(f"ERROR: API Error: {response.status_code}")
            print(f"   {response.text}")
            return None

        result = response.json()
        image_url = result['data'][0]['url']

        # Download the image
        print("Downloading image...")
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code == 200:
            image_filename = f'frame_{frame_id:03d}.png'
            image_path = images_dir / image_filename

            with open(image_path, 'wb') as f:
                f.write(img_response.content)

            print(f"SUCCESS: Image saved: {image_path}")
            return f'images/{image_filename}'
        else:
            print(f"ERROR: Failed to download image")
            return None

    except Exception as e:
        print(f"ERROR: {e}")
        return None

def display_frame_info(frame):
    """Display frame information."""
    print("\n" + "="*70)
    print(f"Frame #{frame['id']}: {frame['reference']}")
    print("="*70)
    print(f"Title: {frame['visualization']['title']}")
    print(f"\nVerse Text:")
    print(f"  \"{frame['text']}\"")

    # Show current image status
    img_path = frame['visualization'].get('imagePath')
    if img_path and os.path.exists(img_path):
        print(f"\nHD Image: {img_path} (exists)")
    elif img_path:
        print(f"\nHD Image: {img_path} (MISSING)")
    else:
        print(f"\nHD Image: None")

    print("\n" + "-"*70)
    print("Current Image Prompt:")
    print("-"*70)
    prompt = get_frame_prompt(frame)
    print(prompt)
    print("-"*70)

def main():
    # Set UTF-8 encoding for Windows
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable frames: 1-592")
        print("\nThis tool allows you to:")
        print("  1. View the prompt used to generate an image")
        print("  2. Edit the prompt in Notepad")
        print("  3. Regenerate the image with your edited prompt")
        sys.exit(1)

    identifier = ' '.join(sys.argv[1:])

    print(f"Loading database...")
    data = load_database()

    frame = find_frame(data, identifier)

    if not frame:
        print(f"\nERROR: Frame not found: {identifier}")
        print("Tip: Use frame ID (1-592) or verse reference (e.g., 'Genesis 1:1')")
        sys.exit(1)

    display_frame_info(frame)

    print("\nOptions:")
    print("  [E] Edit prompt and regenerate image")
    print("  [R] Regenerate image with current prompt")
    print("  [V] View prompt only (no changes)")
    print("  [Q] Quit")

    choice = input("\nYour choice: ").strip().upper()

    if choice == 'Q' or choice == '':
        print("Exiting.")
        sys.exit(0)

    if choice == 'V':
        print("\nPrompt displayed above. No changes made.")
        sys.exit(0)

    current_prompt = get_frame_prompt(frame)

    if choice == 'E':
        # Edit prompt
        edited_prompt = open_in_editor(current_prompt)

        if edited_prompt == current_prompt:
            print("\nNo changes to prompt detected.")
            response = input("Regenerate image anyway? (y/n): ").strip().lower()
            if response != 'y':
                print("Cancelled.")
                sys.exit(0)
        else:
            print("\n" + "="*70)
            print("EDITED PROMPT:")
            print("="*70)
            print(edited_prompt)
            print("="*70)

            response = input("\nSave this prompt and regenerate image? (y/n): ").strip().lower()
            if response != 'y':
                print("Changes discarded.")
                sys.exit(0)

            current_prompt = edited_prompt

    elif choice == 'R':
        response = input("\nRegenerate image with current prompt? (y/n): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            sys.exit(0)
    else:
        print("Invalid choice.")
        sys.exit(1)

    # Generate the image
    image_path = generate_image(current_prompt, frame['id'])

    if image_path:
        # Update the frame in database
        frame['visualization']['imagePrompt'] = current_prompt
        frame['visualization']['imagePath'] = image_path
        frame['timestamp'] = datetime.now().isoformat() + 'Z'

        save_database(data)

        print(f"\nDatabase updated!")
        print(f"  Frame: {frame['id']} ({frame['reference']})")
        print(f"  Image: {image_path}")
        print(f"  Prompt saved to database")
    else:
        print("\nImage generation failed. Database not updated.")

        # Still save the prompt if it was edited
        if choice == 'E' and current_prompt != get_frame_prompt(frame):
            response = input("Save edited prompt anyway (without image)? (y/n): ").strip().lower()
            if response == 'y':
                frame['visualization']['imagePrompt'] = current_prompt
                frame['timestamp'] = datetime.now().isoformat() + 'Z'
                save_database(data)
                print("Prompt saved.")

if __name__ == "__main__":
    main()
