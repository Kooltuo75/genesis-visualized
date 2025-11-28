import json
import sys
from datetime import datetime
from generate_image import generate_image

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def add_verse(reference, text, title, ascii_art):
    """Add a new verse with both ASCII art and HD image"""

    print("=" * 60)
    print(f"Adding new verse: {reference}")
    print("=" * 60)

    # Load current database
    with open('frames-database.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    # Create new frame ID
    frame_id = db['totalFrames'] + 1

    print(f"\nStep 1/3: Creating frame {frame_id}...")

    # Create new frame (without image first)
    new_frame = {
        "id": frame_id,
        "reference": reference,
        "text": text,
        "visualization": {
            "title": title,
            "asciiArt": ascii_art,
            "imagePath": None
        },
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    print(f"Step 2/3: Generating HD image with DALL-E 3...")
    print("(This will take 15-30 seconds...)")

    # Generate HD image
    image_path = generate_image(reference, text, frame_id)

    if image_path:
        new_frame['visualization']['imagePath'] = image_path
        print(f"SUCCESS: HD image created!")
    else:
        print(f"WARNING: Image generation failed, continuing with ASCII only")

    print(f"\nStep 3/3: Saving to database...")

    # Add to database
    db['frames'].append(new_frame)
    db['totalFrames'] = len(db['frames'])
    db['currentFrameIndex'] = len(db['frames']) - 1

    # Save frames database
    with open('frames-database.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    # Update verse-data.json (for live view)
    verse_data = {
        "reference": reference,
        "text": text,
        "visualization": {
            "title": title,
            "asciiArt": ascii_art,
            "imagePath": image_path
        }
    }

    with open('verse-data.json', 'w', encoding='utf-8') as f:
        json.dump(verse_data, f, indent=2, ensure_ascii=False)

    print(f"\n" + "=" * 60)
    print(f"SUCCESS: Frame {frame_id} saved!")
    print(f"Reference: {reference}")
    print(f"ASCII Art: Created")
    print(f"HD Image: {'Created' if image_path else 'Failed'}")
    print("=" * 60)

    return frame_id, image_path

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python add_verse.py <reference> <text> <title> <ascii_art>")
        sys.exit(1)

    reference = sys.argv[1]
    text = sys.argv[2]
    title = sys.argv[3]
    ascii_art = sys.argv[4]

    add_verse(reference, text, title, ascii_art)
