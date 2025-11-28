"""
Frame Listing Tool
List and search frames in the Genesis Bible Visualizer

Usage:
    python list_frames.py                    # List all frames summary
    python list_frames.py <chapter>          # List frames for a chapter
    python list_frames.py search <keyword>   # Search frames by keyword

Examples:
    python list_frames.py 1                  # List Genesis Chapter 1 frames
    python list_frames.py 5                  # List Genesis Chapter 5 frames
    python list_frames.py search Adam        # Find frames mentioning Adam
    python list_frames.py search light       # Find frames mentioning light
"""

import json
import sys

DATABASE_FILE = "frames-database.json"

def load_database():
    """Load the frames database."""
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_chapter(reference):
    """Extract chapter number from verse reference."""
    try:
        # "Genesis 1:1" -> 1
        parts = reference.split()
        chapter_verse = parts[1].split(':')
        return int(chapter_verse[0])
    except:
        return 0

def list_chapter(data, chapter_num):
    """List all frames in a specific chapter."""
    frames = [f for f in data['frames'] if get_chapter(f['reference']) == chapter_num]

    if not frames:
        print(f"\n❌ No frames found for Genesis Chapter {chapter_num}")
        return

    print(f"\n{'='*70}")
    print(f"GENESIS CHAPTER {chapter_num} - {len(frames)} verses")
    print(f"{'='*70}")
    print(f"{'ID':<6} {'Reference':<15} {'Title':<50}")
    print(f"{'-'*70}")

    for frame in frames:
        title = frame['visualization']['title'][:47] + "..." if len(frame['visualization']['title']) > 50 else frame['visualization']['title']
        print(f"{frame['id']:<6} {frame['reference']:<15} {title:<50}")

    print(f"\nTo edit a frame: python edit_ascii.py <frame_id>")

def search_frames(data, keyword):
    """Search frames by keyword in text, title, or reference."""
    keyword_lower = keyword.lower()
    matches = []

    for frame in data['frames']:
        if (keyword_lower in frame['text'].lower() or
            keyword_lower in frame['visualization']['title'].lower() or
            keyword_lower in frame['reference'].lower() or
            keyword_lower in frame['visualization']['asciiArt'].lower()):
            matches.append(frame)

    if not matches:
        print(f"\n❌ No frames found matching '{keyword}'")
        return

    print(f"\n{'='*70}")
    print(f"SEARCH RESULTS: '{keyword}' - {len(matches)} matches")
    print(f"{'='*70}")
    print(f"{'ID':<6} {'Reference':<15} {'Title':<50}")
    print(f"{'-'*70}")

    for frame in matches[:50]:  # Limit to first 50 results
        title = frame['visualization']['title'][:47] + "..." if len(frame['visualization']['title']) > 50 else frame['visualization']['title']
        print(f"{frame['id']:<6} {frame['reference']:<15} {title:<50}")

    if len(matches) > 50:
        print(f"\n... and {len(matches) - 50} more results")

    print(f"\nTo edit a frame: python edit_ascii.py <frame_id>")

def list_summary(data):
    """List summary of all chapters."""
    # Group by chapter
    chapters = {}
    for frame in data['frames']:
        chapter = get_chapter(frame['reference'])
        if chapter not in chapters:
            chapters[chapter] = {'count': 0, 'first_id': frame['id'], 'last_id': frame['id']}
        chapters[chapter]['count'] += 1
        chapters[chapter]['last_id'] = frame['id']

    print(f"\n{'='*60}")
    print(f"GENESIS BIBLE VISUALIZER - FRAME SUMMARY")
    print(f"Total Frames: {len(data['frames'])}")
    print(f"{'='*60}")
    print(f"{'Chapter':<10} {'Verses':<10} {'Frame Range':<20}")
    print(f"{'-'*60}")

    for chapter in sorted(chapters.keys()):
        info = chapters[chapter]
        frame_range = f"{info['first_id']}-{info['last_id']}"
        print(f"Genesis {chapter:<3} {info['count']:<10} {frame_range:<20}")

    print(f"\nUsage:")
    print(f"  python list_frames.py <chapter>        # List chapter frames")
    print(f"  python list_frames.py search <word>   # Search frames")
    print(f"  python edit_ascii.py <frame_id>       # Edit frame ASCII art")

def main():
    data = load_database()

    if len(sys.argv) < 2:
        list_summary(data)
        return

    arg = sys.argv[1]

    # Check for search command
    if arg.lower() == 'search':
        if len(sys.argv) < 3:
            print("Usage: python list_frames.py search <keyword>")
            sys.exit(1)
        keyword = ' '.join(sys.argv[2:])
        search_frames(data, keyword)
        return

    # Try as chapter number
    try:
        chapter_num = int(arg)
        list_chapter(data, chapter_num)
    except ValueError:
        print(f"Unknown command: {arg}")
        print(__doc__)

if __name__ == "__main__":
    main()
