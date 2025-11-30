# Genesis Visualized - Complete Documentation

## Project Overview

**Genesis Visualized** is a multimedia Bible visualization project that presents the Book of Genesis through AI-generated HD images and styled verse cards. The project aims to bring Scripture to life through visual representation, making the biblical narrative more accessible and engaging.

**Mission Statement:** "To God Be The Glory" - This project is offered freely to all who seek to explore God's Word.

---

## Architecture

### Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.x with built-in `http.server` |
| Frontend | Vanilla HTML, CSS, JavaScript |
| Image Generation | OpenAI DALL-E 3 API |
| AI Text Processing | Anthropic Claude API (optional) |
| Cloud Storage | Cloudinary (optional, for deployment) |
| Authentication | Custom session-based auth with SHA-256 hashing |

### Port Configuration

| Service | Default Port | Environment Variable |
|---------|-------------|---------------------|
| API Server | 8003 | `PORT` |
| Static Files | 8005 | `STATIC_PORT` |

---

## File Structure

```
Project 26 - Genesis Visualized/
├── api_server.py          # Main API server (handles all endpoints)
├── auth.py                # Authentication module
├── visualizer.html        # Main visualization interface (74KB)
├── index.html             # Landing page
├── login.html             # User authentication page
├── gallery.html           # Image gallery view
├── frames-database.json   # Main database storing all verses/frames
├── users.json             # User accounts database
├── .env                   # Environment variables (API keys)
├── requirements.txt       # Python dependencies
├── images/                # Generated HD images
│   ├── frame_001.png
│   ├── frame_002.png
│   └── ...
├── Utility Scripts/
│   ├── generate_image.py        # Single image generation
│   ├── batch_generate_images.py # Batch image generation
│   ├── add_verse.py             # Add new verses
│   ├── save_frame.py            # Save frame data
│   ├── edit_ascii.py            # Edit ASCII art
│   ├── edit_prompt.py           # Edit image prompts
│   ├── frame_editor.py          # Frame editing utility
│   ├── list_frames.py           # List all frames
│   ├── optimize_images.py       # Image optimization
│   ├── regenerate_images.py     # Regenerate specific images
│   └── upload_to_cloudinary.py  # Cloud upload utility
├── Chapter Scripts/
│   ├── genesis_chapter_5.py
│   ├── genesis_chapter_6.py
│   └── ... (chapters 7-23)
└── Deployment/
    ├── wsgi.py                  # WSGI entry point for Render
    ├── SETUP_INSTRUCTIONS.md    # Render deployment guide
    └── RENDER_DEPLOYMENT.md     # Detailed deployment docs
```

---

## Database Schema

### frames-database.json

```json
{
  "totalFrames": 267,
  "frames": [
    {
      "id": 1,
      "reference": "Genesis 1:1",
      "text": "In the beginning God created the heavens and the earth.",
      "visualization": {
        "title": "The Moment of Creation",
        "themes": ["Creation", "Divine Power", "Beginning"],
        "notes": "Spiritual insight or historical context...",
        "imagePath": "images/frame_001.png",
        "imagePrompt": "Biblical scene depicting..."
      },
      "timestamp": "2025-11-18T00:00:00Z",
      "currentVersion": 5,
      "versionHistory": [
        {
          "version": 1,
          "timestamp": "2025-11-18T00:00:00Z",
          "title": "...",
          "themes": [],
          "notes": "",
          "imagePrompt": "...",
          "imagePath": "images/frame_001_v1.png"
        }
      ]
    }
  ]
}
```

### users.json

```json
{
  "users": [
    {
      "username": "admin",
      "password_hash": "sha256_hash_here",
      "role": "admin",
      "created": "2025-11-18T00:00:00"
    }
  ]
}
```

---

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/logout` | User logout | Yes |
| GET | `/api/auth/me` | Get current user info | Yes |
| POST | `/api/auth/register` | Create new user | Admin |
| POST | `/api/auth/delete` | Delete user | Admin |
| GET | `/api/auth/users` | List all users | Admin |

### Frame/Verse Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/frames` | List all frames | No |
| GET | `/api/frame/{id}` | Get single frame | No |
| POST | `/api/frame/{id}/save` | Save frame changes (creates version) | Yes |
| POST | `/api/frame/{id}/regenerate` | Regenerate HD image | Yes |
| GET | `/api/frame/{id}/versions` | Get version history | No |
| POST | `/api/frame/{id}/restore` | Restore specific version | Yes |
| POST | `/api/frame/{id}/use-image` | Use image from specific version | Yes |

### Legacy Endpoints (No Version History)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/frame/{id}/ascii` | Update ASCII art only |
| POST | `/api/frame/{id}/prompt` | Update prompt only |
| POST | `/api/frame/{id}/title` | Update title only |

---

## Features

### 1. Verse Card Display (NEW)
Replaces ASCII art with an elegant styled card showing:
- Verse reference and text
- Scene title
- Themed tags (comma-separated)
- Insight/Notes section
- Displayed alongside HD images

### 2. HD Image Generation
- Uses OpenAI DALL-E 3 API
- 1024x1024 resolution
- Customizable prompts per verse
- Automatic image storage

### 3. Version History System
- Automatic versioning on every save
- Image preservation (copies to versioned filename)
- Full restore capability
- Selective restore (image only, or full content)

### 4. User Authentication
- Session-based authentication (24-hour sessions)
- Role-based access (admin, editor)
- Admin panel for user management
- Edit button only visible when logged in

### 5. Navigation Features
- Chapter selector dropdown
- Verse-by-verse navigation (Previous/Next)
- Direct verse input with search
- Position remembered via cookies
- Keyboard shortcuts

### 6. Image Zoom Viewer
- Click-to-zoom functionality
- Pan and zoom controls
- Full-screen viewing

### 7. Gallery Mode
- Browse all images by chapter
- Grid layout display
- Quick navigation

---

## Environment Configuration (.env)

```env
# OpenAI API Configuration (Required for image generation)
OPENAI_API_KEY=sk-proj-xxx

# Anthropic API Configuration (Optional - for AI text formatting)
ANTHROPIC_API_KEY=sk-ant-xxx

# Cloudinary Configuration (Optional - for cloud deployment)
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
USE_CLOUDINARY=false
```

---

## Running the Application

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python api_server.py

# Access the application
# Static files: http://localhost:8005/index.html
# API server: http://localhost:8003
```

### Default Credentials
- **Username:** admin
- **Password:** admin123

---

## Development History

### Session 1: Initial Setup
- Created project structure
- Built basic visualizer with ASCII art display
- Implemented frame database system
- Added image generation with DALL-E 3

### Session 2: Authentication System
- Added user authentication (auth.py)
- Created login page (login.html)
- Implemented session management
- Added admin panel for user management
- Fixed CORS issues with Authorization header

### Session 3: Version History
- Implemented version history system
- Added version snapshots before each edit
- Created restore functionality
- Added "Use Image" selective restore

### Session 4: ASCII Art Tools (Deprecated)
- Built ASCII formatting tools
- Integrated Anthropic Claude API for AI-powered formatting
- Created border fixing algorithms
- Fixed CSS inconsistencies between preview and display

### Session 5: Verse Card Implementation (Current)
- **Replaced ASCII art with styled Verse Card component**
- Added new fields: themes (array), notes (text)
- Updated edit modal with Title, Themes, Notes, Image Prompt
- Updated all API endpoints for new data structure
- Updated version history to store themes/notes
- Fixed empty array handling in theme display

---

## CSS Components

### Verse Card Styling
```css
.verse-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
}

.verse-card-header { /* Reference and title */ }
.verse-card-text { /* Verse text with quotes */ }
.verse-card-themes { /* Theme tags container */ }
.verse-card-theme { /* Individual theme tag */ }
.verse-card-notes { /* Notes section */ }
```

### Color Scheme
- Primary Blue: #1e3c72, #2a5298
- Accent Green: #4CAF50
- Gold Accent: #FFD700
- Sky Blue: #87CEEB

---

## Known Issues & Notes

1. **Image Cache**: Uses cache busting (`?t=timestamp`) for image updates
2. **Session Storage**: In-memory only - sessions lost on server restart
3. **Password Security**: Uses SHA-256 with salt (bcrypt recommended for production)
4. **CORS**: Configured for cross-origin requests between ports 8003/8005

---

## Content Coverage

| Chapter | Verses | Status |
|---------|--------|--------|
| Genesis 1 | 31 | Complete |
| Genesis 2 | 25 | Complete |
| Genesis 3 | 24 | Complete |
| Genesis 4 | 26 | Complete |
| Genesis 5 | 32 | Complete |
| Genesis 6 | 22 | Complete |
| Genesis 7 | 24 | Complete |
| Genesis 8 | 22 | Complete |
| Genesis 9 | 29 | Complete |
| Genesis 10 | 32 | Complete |
| Genesis 11+ | ... | In Progress |

**Total Frames:** 267+ verses with HD images

---

## Future Enhancements

1. **Database Migration**: Move from JSON to SQLite/PostgreSQL
2. **Password Security**: Implement bcrypt hashing
3. **Persistent Sessions**: Redis or database-backed sessions
4. **Search Functionality**: Full-text search across verses
5. **Export Features**: PDF generation, slideshow mode
6. **Mobile App**: React Native or Flutter wrapper
7. **Audio Integration**: Text-to-speech for verses

---

## Credits

- **Scripture Source:** King James Version (KJV)
- **Image Generation:** OpenAI DALL-E 3
- **AI Assistance:** Anthropic Claude
- **Purpose:** For the glory of God

---

*Last Updated: November 30, 2025*
