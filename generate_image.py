import os
import json
import requests
import sys
from datetime import datetime
from pathlib import Path

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def load_api_key():
    """Load OpenAI API key from .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        print("ERROR: .env file not found. Please create one with your OPENAI_API_KEY")
        print("   Example: OPENAI_API_KEY=sk-...")
        return None

    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                key = line.strip().split('=', 1)[1]
                return key

    print("ERROR: OPENAI_API_KEY not found in .env file")
    return None

def create_prompt_from_verse(reference, text):
    """Create a detailed DALL-E prompt from a Bible verse"""

    prompts = {
        "Genesis 1:1": "Epic biblical scene of the creation of the universe, cosmic explosion of light and stars, heavens forming above with galaxies and nebulae, the earth taking shape below with swirling clouds and oceans, divine golden light radiating through space, majestic and awe-inspiring, ultra detailed, cinematic lighting, 8k quality, religious art style",

        "Genesis 1:2": "Dark primordial ocean covered in deep shadows, formless void and chaos, gentle dove-like spirit hovering above turbulent waters, mysterious deep waters stretching endlessly, darkness covering the surface, ethereal divine presence, moody atmospheric lighting, biblical epic scene, ultra detailed, 8k quality",

        "Genesis 1:3": "Brilliant burst of divine light piercing through absolute darkness, first rays of pure golden light illuminating the void, dramatic contrast between light and shadow, God's creation of light, cosmic spiritual scene, radiant beams spreading across space, epic biblical moment, cinematic lighting, 8k quality, religious masterpiece",
    }

    # Return custom prompt if available, otherwise generate generic one
    if reference in prompts:
        return prompts[reference]

    # Generic prompt based on verse content
    return f"Biblical scene depicting: {text}. Epic, cinematic, highly detailed, divine lighting, religious art style, 8k quality"

def generate_image(reference, text, frame_id):
    """Generate an image using DALL-E 3"""

    api_key = load_api_key()
    if not api_key:
        return None

    # Create images directory if it doesn't exist
    images_dir = Path('images')
    images_dir.mkdir(exist_ok=True)

    # Create prompt
    prompt = create_prompt_from_verse(reference, text)

    print(f"Generating image for {reference}...")
    print(f"   Prompt: {prompt[:100]}...")

    # Call DALL-E 3 API
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'dall-e-3',
        'prompt': prompt,
        'n': 1,
        'size': '1024x1024',  # or '1792x1024' for landscape
        'quality': 'hd',
        'style': 'vivid'
    }

    try:
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers=headers,
            json=data,
            timeout=60
        )

        if response.status_code != 200:
            print(f"ERROR: API Error: {response.status_code}")
            print(f"   {response.text}")
            return None

        result = response.json()
        image_url = result['data'][0]['url']

        # Download the image
        img_response = requests.get(image_url, timeout=30)
        if img_response.status_code == 200:
            # Save image with frame ID
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
        print(f"ERROR: Error generating image: {e}")
        return None

if __name__ == "__main__":
    print("Image generation helper loaded.")
    print("Use generate_image(reference, text, frame_id) to create images.")
