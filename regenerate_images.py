import json
import sys
from generate_image import generate_image

sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("REGENERATING HD IMAGES FROM FRAME 138 ONWARDS")
print("="*60)
sys.stdout.flush()

# Load the frames database
with open('frames-database.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

frames = data['frames']

# Find frames that need images (from frame 138 onwards)
frames_to_regenerate = []
for frame in frames:
    frame_id = frame['id']
    if frame_id >= 138:
        # Check if it doesn't have an image or the image path is missing
        if 'imagePath' not in frame['visualization'] or not frame['visualization']['imagePath']:
            frames_to_regenerate.append(frame)

print(f"\nFound {len(frames_to_regenerate)} frames without HD images")
print(f"Frames {frames_to_regenerate[0]['id']} to {frames_to_regenerate[-1]['id']}")
print()

# Regenerate images for each frame
success_count = 0
fail_count = 0

for i, frame in enumerate(frames_to_regenerate, 1):
    frame_id = frame['id']
    reference = frame['reference']
    text = frame['text']

    print(f"[{i}/{len(frames_to_regenerate)}] Regenerating image for Frame {frame_id}: {reference}")

    try:
        image_path = generate_image(reference, text, frame_id)

        if image_path:
            # Update the frame with the new image path
            frame['visualization']['imagePath'] = image_path
            success_count += 1
            print(f"✅ SUCCESS: {image_path}")
        else:
            fail_count += 1
            print(f"❌ FAILED: Could not generate image")
    except Exception as e:
        fail_count += 1
        print(f"❌ ERROR: {str(e)}")

    print()

# Save the updated frames database
print("Saving updated frames database...")
data['frames'] = frames
with open('frames-database.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Update verse-data.json with the last frame
if frames:
    last_frame = frames[-1]
    verse_data = {
        "reference": last_frame['reference'],
        "text": last_frame['text'],
        "visualization": last_frame['visualization']
    }
    with open('verse-data.json', 'w', encoding='utf-8') as f:
        json.dump(verse_data, f, indent=2, ensure_ascii=False)

print("="*60)
print(f"REGENERATION COMPLETE!")
print(f"Success: {success_count}")
print(f"Failed: {fail_count}")
print(f"Total processed: {len(frames_to_regenerate)}")
print("="*60)
