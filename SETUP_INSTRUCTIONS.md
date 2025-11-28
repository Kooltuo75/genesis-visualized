# Bible Verse Visualizer - Setup Instructions

## Image Generation with DALL-E 3

Your visualizer now supports HD image generation alongside ASCII art!

### Setup Steps:

#### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Create .env File
Create a file named `.env` in this directory with your OpenAI API key:

```
OPENAI_API_KEY=sk-your-api-key-here
```

**To get an OpenAI API key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and paste it into your `.env` file

**Note:** The `.env` file is protected by `.gitignore` so your API key won't be committed to git.

#### 3. You're Ready!

Now when you type a Bible verse to Claude, it will:
1. Create the ASCII art visualization
2. Automatically generate an HD image using DALL-E 3
3. Display both side-by-side in the visualizer
4. Save both to the frames database

### Cost Information:

- DALL-E 3 HD images: ~$0.080 per image (1024x1024)
- DALL-E 3 Standard images: ~$0.040 per image (1024x1024)

The current setup uses HD quality for best results.

### How It Works:

When you type a verse, I will:
1. Update `verse-data.json` with the verse and ASCII art
2. Call the image generation script to create an HD image
3. Save the image to the `images/` folder
4. Update the database with both visualizations

### Files Created:

- `.env` - Your API key (keep this secret!)
- `generate_image.py` - Script to generate DALL-E images
- `images/` - Folder where HD images are saved
- `.gitignore` - Protects your API key from being committed

### Troubleshooting:

**Images not generating?**
- Check that `.env` file exists and has your API key
- Verify Python dependencies are installed
- Check console for error messages

**Images taking too long?**
- DALL-E 3 typically takes 10-30 seconds per image
- Check your OpenAI API quota/billing

Ready to continue! Just paste your OpenAI API key into a `.env` file and we'll start generating beautiful HD images for each verse.
