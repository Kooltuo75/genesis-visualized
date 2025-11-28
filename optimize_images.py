"""
Image Optimizer for Genesis Bible Visualizer
=============================================
Creates compressed web-optimized versions of HD images.

Original: ~1.7-2.2 MB PNG (1024x1024)
Optimized: ~100-200 KB WebP (800x800)

Usage:
    python optimize_images.py          # Optimize all images
    python optimize_images.py 1 50     # Optimize frames 1-50
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow not installed. Installing...")
    os.system('pip install Pillow')
    from PIL import Image

IMAGES_DIR = Path("images")
WEB_DIR = Path("images_web")
TARGET_SIZE = (800, 800)  # Good balance of quality and speed
QUALITY = 85  # WebP quality (0-100)

def optimize_image(frame_id):
    """Optimize a single image."""
    src_path = IMAGES_DIR / f"frame_{frame_id:03d}.png"
    dst_path = WEB_DIR / f"frame_{frame_id:03d}.webp"

    if not src_path.exists():
        return None

    if dst_path.exists():
        return "skipped"

    try:
        with Image.open(src_path) as img:
            # Resize if larger than target
            if img.size[0] > TARGET_SIZE[0] or img.size[1] > TARGET_SIZE[1]:
                img.thumbnail(TARGET_SIZE, Image.Resampling.LANCZOS)

            # Convert to RGB if necessary (WebP doesn't support all modes)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

            # Save as WebP
            img.save(dst_path, 'WEBP', quality=QUALITY, method=6)

        src_size = src_path.stat().st_size / 1024
        dst_size = dst_path.stat().st_size / 1024
        reduction = (1 - dst_size/src_size) * 100

        return f"{src_size:.0f}KB -> {dst_size:.0f}KB ({reduction:.0f}% smaller)"
    except Exception as e:
        return f"error: {e}"

def main():
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')

    # Create web directory
    WEB_DIR.mkdir(exist_ok=True)

    # Determine range
    start, end = 1, 592
    if len(sys.argv) >= 3:
        start, end = int(sys.argv[1]), int(sys.argv[2])
    elif len(sys.argv) == 2:
        start = end = int(sys.argv[1])

    print(f"Optimizing frames {start}-{end}...")
    print(f"Target: {TARGET_SIZE[0]}x{TARGET_SIZE[1]} WebP @ {QUALITY}% quality")
    print("-" * 50)

    optimized = 0
    skipped = 0
    missing = 0

    for frame_id in range(start, end + 1):
        result = optimize_image(frame_id)

        if result is None:
            missing += 1
        elif result == "skipped":
            skipped += 1
            print(f"Frame {frame_id}: already optimized")
        elif result.startswith("error"):
            print(f"Frame {frame_id}: {result}")
        else:
            optimized += 1
            print(f"Frame {frame_id}: {result}")

    print("-" * 50)
    print(f"Done! Optimized: {optimized}, Skipped: {skipped}, Missing: {missing}")
    print(f"\nOptimized images saved to: {WEB_DIR.absolute()}")

if __name__ == "__main__":
    main()
