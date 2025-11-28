"""
Upload Existing Images to Cloudinary
=====================================
Run this script after setting up Cloudinary credentials in .env
to upload all existing local images to the cloud.

Usage: python upload_to_cloudinary.py
"""

import json
import os
from pathlib import Path

# Load environment from .env
def load_env():
    env_vars = {}
    env_path = Path('.env')
    if env_path.exists():
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

env = load_env()

# Check if Cloudinary is configured
use_cloudinary = env.get('USE_CLOUDINARY', 'false')
if use_cloudinary != 'true':
    print("Cloudinary is not enabled. Set USE_CLOUDINARY=true in .env")
    print("Then fill in your Cloudinary credentials from https://cloudinary.com/console")
    exit(1)

cloud_name = env.get('CLOUDINARY_CLOUD_NAME')
api_key = env.get('CLOUDINARY_API_KEY')
api_secret = env.get('CLOUDINARY_API_SECRET')

if not all([cloud_name, api_key, api_secret]) or cloud_name == 'your_cloud_name':
    print("Cloudinary credentials not configured in .env")
    print("Please fill in:")
    print("  CLOUDINARY_CLOUD_NAME=your_cloud_name")
    print("  CLOUDINARY_API_KEY=your_api_key")
    print("  CLOUDINARY_API_SECRET=your_api_secret")
    exit(1)

# Import cloudinary
try:
    import cloudinary
    import cloudinary.uploader
except ImportError:
    print("Cloudinary not installed. Run: pip install cloudinary")
    exit(1)

# Configure Cloudinary
cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)

print(f"Cloudinary configured: {cloud_name}")

# Load database
DATABASE_FILE = "frames-database.json"
IMAGES_DIR = Path("images")

with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

uploaded_count = 0
updated_paths = []

for frame in data['frames']:
    viz = frame.get('visualization', {})
    image_path = viz.get('imagePath', '')

    # Skip if already a Cloudinary URL
    if image_path.startswith('http'):
        print(f"Frame {frame['id']}: Already cloud URL, skipping")
        continue

    # Skip if no image
    if not image_path:
        print(f"Frame {frame['id']}: No image")
        continue

    # Check if local file exists
    local_path = Path(image_path)
    if not local_path.exists():
        print(f"Frame {frame['id']}: Local file not found: {image_path}")
        continue

    # Upload to Cloudinary
    frame_id = frame['id']
    public_id = f'frame_{frame_id:03d}'

    try:
        print(f"Frame {frame_id}: Uploading {image_path}...")
        result = cloudinary.uploader.upload(
            str(local_path),
            public_id=public_id,
            folder='genesis-visualized',
            resource_type='image',
            overwrite=True
        )

        cloudinary_url = result['secure_url']
        frame['visualization']['imagePath'] = cloudinary_url
        updated_paths.append((frame_id, cloudinary_url))
        uploaded_count += 1
        print(f"  -> {cloudinary_url}")

    except Exception as e:
        print(f"  ERROR: {e}")

# Save updated database
if uploaded_count > 0:
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"\nUploaded {uploaded_count} images to Cloudinary")
    print("Database updated with cloud URLs")
else:
    print("\nNo images uploaded")

# Also upload version history images
print("\nChecking version history images...")
for frame in data['frames']:
    for version in frame.get('versionHistory', []):
        image_path = version.get('imagePath', '')

        # Skip cloud URLs and empty paths
        if not image_path or image_path.startswith('http'):
            continue

        local_path = Path(image_path)
        if not local_path.exists():
            continue

        # Generate unique public_id for version
        frame_id = frame['id']
        version_num = version['version']
        public_id = f'frame_{frame_id:03d}_v{version_num}'

        try:
            print(f"Frame {frame_id} v{version_num}: Uploading...")
            result = cloudinary.uploader.upload(
                str(local_path),
                public_id=public_id,
                folder='genesis-visualized',
                resource_type='image',
                overwrite=True
            )
            version['imagePath'] = result['secure_url']
            print(f"  -> {result['secure_url']}")
        except Exception as e:
            print(f"  ERROR: {e}")

# Save database again with version history updates
with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nDone!")
