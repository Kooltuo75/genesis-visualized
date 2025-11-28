# GENESIS VISUALIZED - Complete Project Documentation

> **Last Updated**: 2025-11-28
> **Current Progress**: 592 frames (Genesis 1:1 - 23:20) = 38.6% complete
> **Total Genesis Verses**: 1,533

---

## PROJECT OVERVIEW

**Genesis Visualized** is an ambitious digital humanities project that transforms the Book of Genesis (KJV) into an immersive multimedia experience. Each verse receives:

1. **HD AI-Generated Artwork** - DALL-E 3 images (1024x1024, ~1.8MB each)
2. **ASCII Art Visualization** - Creative Unicode/emoji representations
3. **Interactive Web Galleries** - Multiple viewing modes
4. **Editing & Version Control** - Full revision history with rollback

This is NOT a simple project - it's a production-quality application with sophisticated architecture, version control, and professional UI/UX design.

---

## QUICK STATS

| Metric | Value |
|--------|-------|
| Total Frames Created | 592 |
| Chapters Complete | 1-23 (of 50) |
| HD Images Generated | 458 |
| Images Pending | 134 |
| Database Size | 676 KB |
| Images Directory | 818 MB |
| Cost Estimate | ~$366 (at $0.80/image) |

---

## ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────────┐
│                        GENESIS VISUALIZED                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐         │
│   │   FRONTEND   │    │   BACKEND    │    │    DATA      │         │
│   │              │    │              │    │              │         │
│   │ index.html   │◄──►│ api_server   │◄──►│ frames-db    │         │
│   │ visualizer   │    │   .py        │    │   .json      │         │
│   │ gallery.html │    │              │    │              │         │
│   └──────────────┘    └──────────────┘    └──────────────┘         │
│          │                   │                   │                  │
│          │                   ▼                   │                  │
│          │            ┌──────────────┐           │                  │
│          │            │  DALL-E 3    │           │                  │
│          │            │    API       │           │                  │
│          │            └──────────────┘           │                  │
│          │                   │                   │                  │
│          │                   ▼                   │                  │
│          │            ┌──────────────┐           │                  │
│          └───────────►│   images/    │◄──────────┘                  │
│                       │  (458 PNGs)  │                              │
│                       └──────────────┘                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## FILE STRUCTURE

```
Project 26 - Genesis - Copy (2)/
│
├── DATA FILES
│   ├── frames-database.json      # Master database (592 frames, 676KB)
│   └── verse-data.json           # Last processed verse cache
│
├── WEB INTERFACES
│   ├── index.html                # Landing page with live stats
│   ├── visualizer.html           # Main reader with editing
│   ├── gallery.html              # Grid gallery with chapter nav
│   └── bible-visualizer.html     # Alternative verse input tool
│
├── PYTHON CORE
│   ├── api_server.py             # REST API server (18KB)
│   ├── generate_image.py         # DALL-E 3 integration (4.3KB)
│   ├── add_verse.py              # Verse pipeline (2.7KB)
│   └── save_frame.py             # Frame creation helper
│
├── MANAGEMENT TOOLS
│   ├── frame_editor.py           # Comprehensive CLI editor (18.9KB)
│   ├── edit_ascii.py             # Quick ASCII editor
│   ├── edit_prompt.py            # Image prompt editor (10.2KB)
│   ├── list_frames.py            # Search & browse frames
│   ├── optimize_images.py        # PNG→WebP compression
│   └── regenerate_images.py      # Batch image regeneration
│
├── CHAPTER GENERATORS
│   ├── genesis_chapter_1.py      # through genesis_chapter_23.py
│   ├── genesis_chapter_11_part2.py
│   ├── genesis_chapter_12_full.py
│   └── batch_chapters_15_to_25.py
│
├── IMAGES
│   └── images/                   # 458 HD PNG files (818MB total)
│       ├── frame_001.png
│       ├── frame_002.png
│       └── ... frame_509.png
│
├── CONFIG & DOCS
│   ├── .env                      # OPENAI_API_KEY (gitignored)
│   ├── requirements.txt          # Python dependencies
│   ├── start_server.bat          # Windows server launcher
│   ├── PROJECT_STATUS.md         # Session notes
│   └── SETUP_INSTRUCTIONS.md     # API setup guide
│
└── .claude/
    └── settings.local.json       # Claude Code permissions
```

---

## DATABASE SCHEMA

### frames-database.json Structure

```json
{
  "totalFrames": 592,
  "currentFrameIndex": 591,
  "frames": [
    {
      "id": 1,
      "reference": "Genesis 1:1",
      "text": "In the beginning God created the heavens and the earth.",
      "visualization": {
        "title": "The Moment of Creation",
        "asciiArt": "✨ ╔═══════════════════╗ ...",
        "imagePath": "images/frame_001.png",
        "imagePrompt": "Epic biblical scene...",
        "currentVersion": 1,
        "versionHistory": [
          {
            "version": 1,
            "timestamp": "2025-11-18T00:00:00Z",
            "title": "...",
            "asciiArt": "...",
            "imagePrompt": "...",
            "imagePath": "..."
          }
        ]
      },
      "timestamp": "2025-11-18T00:00:00Z"
    }
  ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | int | Sequential frame number (1-592) |
| `reference` | string | Bible verse reference (e.g., "Genesis 1:1") |
| `text` | string | Full KJV verse text |
| `visualization.title` | string | Artistic title for the scene |
| `visualization.asciiArt` | string | Multi-line ASCII art |
| `visualization.imagePath` | string/null | Path to HD image |
| `visualization.imagePrompt` | string | DALL-E 3 prompt used |
| `visualization.currentVersion` | int | Current version number |
| `visualization.versionHistory` | array | All previous versions |
| `timestamp` | string | ISO 8601 timestamp |

---

## API ENDPOINTS

**Server URL**: `http://localhost:8003` (API) / `http://localhost:8005` (Static)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/frame/{id}` | Get frame with prompt |
| GET | `/api/frame/{id}/versions` | Get version history |
| POST | `/api/frame/{id}/save` | Save all changes (creates version) |
| POST | `/api/frame/{id}/regenerate` | Generate new image via DALL-E 3 |
| POST | `/api/frame/{id}/restore` | Restore previous version |
| POST | `/api/frame/{id}/ascii` | Update ASCII art only |
| POST | `/api/frame/{id}/prompt` | Update prompt only |
| POST | `/api/frame/{id}/title` | Update title only |

### API Response Format

```json
{
  "success": true,
  "frame": { /* frame object */ },
  "message": "Frame updated successfully"
}
```

---

## WEB INTERFACES

### 1. Landing Page (index.html)

**Features:**
- Hero section with animated logo
- Live statistics from database (verses, chapters, images)
- Feature cards grid (6 cards)
- CTA buttons to visualizer/gallery
- Gradient background with pulse animations

**Data Interaction:** Fetches `frames-database.json` for live stats

### 2. Main Visualizer (visualizer.html)

**Features:**
- Full-screen frame display
- Side-by-side ASCII art + HD image
- Chapter quick-navigation bar
- Frame navigation (Previous/Next/Begin/End)
- Edit modal with version history
- Image fullscreen mode
- Download options (image, ASCII, full frame HTML)
- Keyboard shortcuts (arrows, Home/End, E for edit, Escape)
- Position memory via cookies
- Image preloading (3 frames ahead/behind)
- Live polling mode when at last frame

**Keyboard Shortcuts:**
- `←` / `→` - Navigate frames
- `Home` / `End` - First/last frame
- `E` - Open edit modal
- `Escape` - Close modals

### 3. Gallery View (gallery.html)

**Features:**
- Responsive 3-column grid (adjusts to screen size)
- Frame cards with:
  - Frame number badge
  - Chapter badge
  - Verse reference & text preview
  - Image thumbnail
  - ASCII preview
- Chapter filter buttons
- Modal frame viewer with full details
- Fullscreen image viewer
- Download capabilities

### 4. Verse Input Tool (bible-visualizer.html)

**Features:**
- Manual verse input field
- Real-time ASCII art generation
- Pattern-matched descriptions
- Template system for special verses (Genesis 1:1-1:3)
- Verse history display

---

## PYTHON TOOLS

### Core Processing

#### add_verse.py
```python
add_verse(reference, text, title, ascii_art)
```
Main pipeline for adding new verses:
1. Creates frame with auto-incremented ID
2. Calls DALL-E 3 for HD image
3. Saves to frames-database.json
4. Updates verse-data.json

#### generate_image.py
```python
generate_image(reference, text, frame_id)
```
- Loads API key from .env
- Creates/uses custom prompts for Genesis 1:1-1:3
- Calls DALL-E 3 (HD quality, 1024x1024, vivid style)
- Downloads and saves image as PNG

#### api_server.py
- Dual HTTP server (API on 8003, static on 8005)
- Full REST API for frame operations
- Version control system
- Image regeneration via DALL-E 3

### Management Tools

#### frame_editor.py
Interactive CLI for quality control:
- Navigate frames (next/prev/jump/search)
- Edit title, ASCII art, prompt
- Regenerate images
- Version history management
- Opens Notepad for editing
- Change tracking with save confirmation

**Commands:**
```
[N]ext  [P]rev  [J]ump  [S]earch  [G]o to frame
[1]Title  [2]ASCII  [3]Prompt  [4]Regenerate
[V]iew Full  [O]pen Image  [W]Save  [Q]uit
```

#### list_frames.py
```bash
python list_frames.py              # Chapter summary
python list_frames.py 1            # List Genesis 1 frames
python list_frames.py search light # Search for "light"
```

#### optimize_images.py
Converts PNG to WebP:
- Input: 1024x1024 PNG (~1.8MB)
- Output: 800x800 WebP (~150KB)
- ~95% size reduction

---

## CHAPTER PROGRESS

| Chapter | Verses | Frames | Status |
|---------|--------|--------|--------|
| 1 | 31 | 1-31 | Complete |
| 2 | 25 | 32-56 | Complete |
| 3 | 24 | 57-80 | Complete |
| 4 | 26 | 81-106 | Complete |
| 5 | 32 | 107-138 | Complete |
| 6 | 22 | 139-160 | Complete |
| 7 | 24 | 161-184 | Complete |
| 8 | 22 | 185-206 | Complete |
| 9 | 29 | 207-235 | Complete |
| 10 | 32 | 236-267 | Complete |
| 11 | 32 | 268-299 | Complete |
| 12 | 20 | 300-319 | Complete |
| 13 | 18 | 320-337 | Complete |
| 14 | 24 | 338-361 | Complete |
| 15 | 21 | 362-382 | Complete |
| 16 | 16 | 383-398 | Complete |
| 17 | 27 | 399-425 | Complete |
| 18 | 33 | 426-458 | Complete |
| 19 | 38 | 459-496 | Complete |
| 20 | 18 | 497-514 | Complete |
| 21 | 34 | 515-548 | Complete |
| 22 | 24 | 549-572 | Complete |
| 23 | 20 | 573-592 | Complete |
| 24-50 | 941 | - | **PENDING** |

**Remaining Work:** 941 verses across 27 chapters

---

## COOL FEATURES TO PRESERVE

### 1. Version Control System
Every frame edit creates immutable snapshots. Users can:
- View all previous versions with timestamps
- See what changed (title, ASCII, prompt, image)
- Restore any previous version
- Track edit history over time

### 2. Dual Media Approach
Combines retro ASCII art with cutting-edge AI imagery:
- ASCII art uses Unicode box-drawing and emojis
- DALL-E 3 images are HD quality with vivid style
- Both displayed side-by-side for unique aesthetic

### 3. Custom Prompt System
Special hand-crafted prompts for key verses:
```python
CUSTOM_PROMPTS = {
    "Genesis 1:1": "Epic biblical scene of the creation of the universe,
                   cosmic explosion of light and stars, heavens forming
                   above with galaxies and nebulae...",
    "Genesis 1:2": "Vast primordial ocean of deep waters, divine spirit
                   hovering as ethereal light above dark abyss...",
    "Genesis 1:3": "Moment of divine command, blazing holy light bursting
                   through absolute darkness..."
}
```

### 4. Smart Navigation
- Image preloading (3 frames ahead/behind)
- Cookie-based position memory
- Keyboard shortcuts for power users
- Chapter quick-jump buttons
- Live polling mode at last frame

### 5. Multiple View Modes
- **Visualizer**: Frame-by-frame reader
- **Gallery**: Grid overview with chapter filtering
- **Fullscreen**: Image-only mode
- **Edit Modal**: In-place editing with version control

### 6. Download Capabilities
- Download individual HD images
- Download ASCII art as text files
- Download complete standalone HTML frames (embedded base64 image)

### 7. Responsive Design
- Desktop: Full 3-column layouts
- Tablet: 2-column grids
- Mobile: Single column with touch-friendly controls

### 8. Professional UI/UX
- Frosted glass effects (backdrop-filter blur)
- Smooth transitions (0.3s cubic-bezier)
- Staggered fade-in animations
- Shadow depth effects
- Color-coded badges and status indicators

### 9. Graceful Degradation
- Works offline (static JSON loading)
- Fallback when API unavailable
- Shows placeholders for missing images
- Error handling throughout

### 10. Batch Processing
- Chapter-by-chapter script execution
- Subprocess orchestration
- Progress tracking
- Automatic image generation pipeline

---

## HOW TO START THE PROJECT

### Option 1: Full Server Mode (Recommended)
```bash
# Start the API server
python api_server.py

# Or use the batch file
start_server.bat

# Access:
# - http://localhost:8005/index.html (Landing page)
# - http://localhost:8005/visualizer.html (Reader)
# - http://localhost:8005/gallery.html (Gallery)
```

### Option 2: Static Mode (No Editing)
Simply open `index.html` directly in a browser. Navigation and viewing work, but editing features require the API server.

---

## HOW TO ADD NEW VERSES

### Method 1: Chapter Script
```python
# Create genesis_chapter_24.py
from add_verse import add_verse

add_verse(
    reference="Genesis 24:1",
    text="And Abraham was old, and well stricken in age...",
    title="Abraham's Old Age",
    ascii_art="""
    ═══════════════════════════════════════════════
              👴 ABRAHAM'S OLD AGE 👴
    ═══════════════════════════════════════════════
    """
)
```

### Method 2: Using frame_editor.py
```bash
python frame_editor.py
# Navigate to last frame, use commands to add/edit
```

### Method 3: Direct API
```bash
curl -X POST http://localhost:8003/api/frame/new \
  -H "Content-Type: application/json" \
  -d '{"reference": "Genesis 24:1", ...}'
```

---

## TROUBLESHOOTING

### API Key Issues
```bash
python test_api_key.py
```
This validates your OpenAI API key and checks DALL-E 3 access.

### Missing Images
```bash
python regenerate_images.py
```
Regenerates all frames that have null imagePath.

### Image Optimization
```bash
python optimize_images.py
```
Creates WebP versions for faster web loading.

### Database Corruption
Always backup `frames-database.json` before major operations. The database is plain JSON and can be manually edited if needed.

---

## DEPENDENCIES

### Python Requirements
```
requests>=2.31.0        # HTTP requests for API calls
python-dotenv>=1.0.0    # Load environment variables
Pillow                  # Image optimization (optional)
```

### Environment Setup
```bash
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

---

## COST ESTIMATES

| Item | Cost | Notes |
|------|------|-------|
| DALL-E 3 HD Image | $0.080 | 1024x1024 HD quality |
| Current Images (458) | ~$36.64 | Already generated |
| Remaining Images (134) | ~$10.72 | Frames with null path |
| Remaining Chapters (941) | ~$75.28 | Chapters 24-50 |
| **Total Remaining** | **~$86.00** | To complete Genesis |

---

## BACKUP CHECKLIST

Essential files to backup:
- [ ] `frames-database.json` - All verse data and metadata
- [ ] `images/` folder - All 458 HD PNG images (818MB)
- [ ] `.env` - API key (keep secure!)
- [ ] All `*.py` scripts - Processing pipeline
- [ ] All `*.html` files - Web interfaces

---

## NEXT STEPS TO CONTINUE

1. **Generate missing images (134 frames)**
   ```bash
   python batch_generate_images.py
   ```

2. **Create Genesis Chapter 24** (67 verses - longest chapter!)
   - Copy pattern from `genesis_chapter_23.py`
   - Add all 67 verses with ASCII art
   - Run script to generate images

3. **Continue through Chapter 50**
   - 941 verses remaining
   - ~27 more chapter scripts needed

4. **Quality Review**
   - Use `frame_editor.py` to review frames
   - Regenerate any subpar images
   - Polish ASCII art designs

---

## CONTACT & CREDITS

This project uses:
- **OpenAI DALL-E 3** for AI image generation
- **King James Version (KJV)** Bible text
- **Pure HTML/CSS/JavaScript** frontend
- **Python** backend processing

---

*Documentation auto-generated and maintained for easy project resumption.*
