# Deploying Genesis Visualized to Render

## Prerequisites

1. **GitHub Repository**: Your code is at https://github.com/Kooltuo75/genesis-visualized
2. **Render Account**: Create a free account at https://render.com
3. **Cloudinary Account**: Create a free account at https://cloudinary.com (for image storage)

## Step 1: Set Up Cloudinary

1. Go to https://cloudinary.com and sign up (free tier available)
2. Once logged in, go to the **Dashboard**
3. Copy these values:
   - Cloud Name
   - API Key
   - API Secret

## Step 2: Deploy to Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Web Service**
3. Connect your GitHub account if not already connected
4. Select the `genesis-visualized` repository
5. Configure the service:
   - **Name**: genesis-visualized
   - **Region**: Choose closest to you
   - **Branch**: master
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 wsgi:application`

6. Click **Advanced** and add these **Environment Variables**:

   | Key | Value |
   |-----|-------|
   | OPENAI_API_KEY | Your OpenAI API key |
   | CLOUDINARY_CLOUD_NAME | Your Cloudinary cloud name |
   | CLOUDINARY_API_KEY | Your Cloudinary API key |
   | CLOUDINARY_API_SECRET | Your Cloudinary API secret |
   | USE_CLOUDINARY | true |

7. Click **Create Web Service**

## Step 3: Upload Existing Images (Optional)

If you have local images you want to migrate to Cloudinary:

1. Update your local `.env` file with Cloudinary credentials
2. Set `USE_CLOUDINARY=true`
3. Run: `python upload_to_cloudinary.py`

This will upload all existing images and update the database with cloud URLs.

## Step 4: Access Your Site

Once deployed, Render will give you a URL like:
`https://genesis-visualized.onrender.com`

### Default Login
- Username: `admin`
- Password: `admin123`

**Important**: Change the admin password after first login!

## Managing Users

As admin, you can:
1. Go to `/login.html`
2. Sign in with admin credentials
3. Use the Admin Panel to:
   - Add new users (editors or admins)
   - Delete users
   - View all registered users

## Troubleshooting

### Images not loading
- Ensure Cloudinary credentials are correct
- Check that `USE_CLOUDINARY=true` is set
- Run `upload_to_cloudinary.py` to migrate local images

### Authentication issues
- The `users.json` file is created on first run
- If you lose access, delete `users.json` and restart - it will recreate the default admin

### Build failures
- Ensure all dependencies are in `requirements.txt`
- Check Render logs for specific errors

## Local Development

To run locally:
```bash
# Install dependencies
pip install -r requirements.txt

# Copy example env
cp .env.example .env

# Edit .env with your API keys
notepad .env

# Start the server
python api_server.py
```

Then open: http://localhost:8005/visualizer.html
