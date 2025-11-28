import json
import sys
from generate_image import generate_image

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load the frames database
with open('frames-database.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print("=" * 60)
print("Generating HD images for existing frames...")
print("=" * 60)

# Generate images for each frame that doesn't have one
for frame in db['frames']:
    if not frame['visualization'].get('imagePath'):
        print(f"\nFrame {frame['id']}: {frame['reference']}")

        image_path = generate_image(
            frame['reference'],
            frame['text'],
            frame['id']
        )

        if image_path:
            frame['visualization']['imagePath'] = image_path
            print(f"SUCCESS: Added image to Frame {frame['id']}")
        else:
            print(f"FAILED: Could not generate image for Frame {frame['id']}")
    else:
        print(f"SKIP: Frame {frame['id']} already has an image")

# Save updated database
with open('frames-database.json', 'w', encoding='utf-8') as f:
    json.dump(db, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 60)
print("Batch generation complete!")
print("=" * 60)

# Also update verse-data.json with the latest frame's image
latest_frame = db['frames'][-1]
with open('verse-data.json', 'r', encoding='utf-8') as f:
    verse_data = json.load(f)

if verse_data['reference'] == latest_frame['reference']:
    verse_data['visualization']['imagePath'] = latest_frame['visualization'].get('imagePath')
    with open('verse-data.json', 'w', encoding='utf-8') as f:
        json.dump(verse_data, f, indent=2, ensure_ascii=False)
    print(f"Updated verse-data.json with image for {latest_frame['reference']}")
