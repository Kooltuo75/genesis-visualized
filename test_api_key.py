import requests
import sys
from pathlib import Path

# Set UTF-8 encoding for console output on Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def load_api_key():
    """Load OpenAI API key from .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        print("ERROR: .env file not found")
        return None

    with open('.env', 'r') as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                key = line.strip().split('=', 1)[1]
                return key
    return None

print("=" * 60)
print("OpenAI API Key Test")
print("=" * 60)

api_key = load_api_key()
if not api_key:
    print("ERROR: Could not load API key from .env file")
    sys.exit(1)

print(f"\nAPI Key loaded: {api_key[:20]}...{api_key[-4:]}")

# Test 1: Check if key is valid by listing models
print("\n--- Test 1: Checking API Access ---")
headers = {
    'Authorization': f'Bearer {api_key}',
}

try:
    response = requests.get(
        'https://api.openai.com/v1/models',
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        print("SUCCESS: API key is valid and working!")
        models = response.json()
        print(f"Available models count: {len(models.get('data', []))}")
    else:
        print(f"ERROR: Status {response.status_code}")
        print(f"Response: {response.text}")

except Exception as e:
    print(f"ERROR: {e}")

# Test 2: Try to get account/billing info
print("\n--- Test 2: Checking Image Generation Access ---")
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

data = {
    'model': 'dall-e-3',
    'prompt': 'A simple test image of a red cube',
    'n': 1,
    'size': '1024x1024',
    'quality': 'standard',  # Using standard instead of HD to reduce cost
    'style': 'vivid'
}

try:
    response = requests.post(
        'https://api.openai.com/v1/images/generations',
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code == 200:
        print("SUCCESS: Image generation works!")
        print("Your API key has access to DALL-E 3")
    else:
        print(f"ERROR: Status {response.status_code}")
        error_data = response.json()
        print(f"Error message: {error_data.get('error', {}).get('message', 'Unknown error')}")
        print(f"Error type: {error_data.get('error', {}).get('type', 'Unknown')}")
        print(f"Error code: {error_data.get('error', {}).get('code', 'Unknown')}")

        if 'billing' in str(error_data).lower():
            print("\n>>> BILLING ISSUE DETECTED <<<")
            print("Please check:")
            print("1. https://platform.openai.com/settings/organization/billing")
            print("2. Ensure you have a payment method added")
            print("3. Check your spending limits aren't set to $0")
            print("4. Verify your monthly budget is sufficient")

except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)
