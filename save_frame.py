import json
from datetime import datetime

def save_frame(reference, text, title, ascii_art):
    """Save a new frame to the frames database"""

    # Read current database
    with open('frames-database.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

    # Create new frame
    new_frame = {
        "id": db['totalFrames'] + 1,
        "reference": reference,
        "text": text,
        "visualization": {
            "title": title,
            "asciiArt": ascii_art
        },
        "timestamp": datetime.utcnow().isoformat() + 'Z'
    }

    # Add to database
    db['frames'].append(new_frame)
    db['totalFrames'] = len(db['frames'])
    db['currentFrameIndex'] = len(db['frames']) - 1

    # Save database
    with open('frames-database.json', 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    print(f"✅ Frame {new_frame['id']} saved: {reference}")
    return new_frame['id']

if __name__ == "__main__":
    print("Frame save helper loaded. Use save_frame() to add new frames.")
