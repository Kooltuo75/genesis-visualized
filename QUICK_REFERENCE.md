# QUICK REFERENCE - Genesis Visualized

> Fast lookup for common tasks. See PROJECT_DOCUMENTATION.md for full details.

---

## START THE PROJECT

```bash
# Start servers (API + Static)
python api_server.py
# OR
start_server.bat

# Then open:
# http://localhost:8005/index.html
```

---

## COMMON COMMANDS

| Task | Command |
|------|---------|
| Start server | `python api_server.py` |
| Test API key | `python test_api_key.py` |
| List all frames | `python list_frames.py` |
| List chapter N | `python list_frames.py N` |
| Search frames | `python list_frames.py search KEYWORD` |
| Edit frames | `python frame_editor.py` |
| Generate missing images | `python batch_generate_images.py` |
| Optimize images | `python optimize_images.py` |

---

## ADD A NEW VERSE

```python
from add_verse import add_verse

add_verse(
    reference="Genesis 24:1",
    text="And Abraham was old...",
    title="Abraham's Old Age",
    ascii_art="""
    ═══════════════════════════════════════════════
              👴 ABRAHAM'S OLD AGE 👴
    ═══════════════════════════════════════════════
    """
)
```

---

## FRAME EDITOR COMMANDS

```
[N]ext      - Next frame
[P]rev      - Previous frame
[J]ump      - Jump to frame ID
[S]earch    - Search frames
[1]         - Edit title
[2]         - Edit ASCII art
[3]         - Edit prompt
[4]         - Regenerate image
[V]         - View full content
[O]         - Open image
[W]         - Save changes
[Q]         - Quit
```

---

## KEYBOARD SHORTCUTS (Visualizer)

| Key | Action |
|-----|--------|
| `←` | Previous frame |
| `→` | Next frame |
| `Home` | First frame |
| `End` | Last frame |
| `E` | Open edit modal |
| `Escape` | Close modal |

---

## FILE LOCATIONS

| File | Purpose |
|------|---------|
| `frames-database.json` | Main database (592 frames) |
| `verse-data.json` | Last processed verse |
| `images/` | HD PNG images (818MB) |
| `.env` | API key storage |

---

## API ENDPOINTS (localhost:8003)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/frame/{id}` | GET | Get frame data |
| `/api/frame/{id}/versions` | GET | Get version history |
| `/api/frame/{id}/save` | POST | Save changes |
| `/api/frame/{id}/regenerate` | POST | New image |
| `/api/frame/{id}/restore` | POST | Restore version |

---

## CURRENT PROGRESS

- **Frames Complete**: 592 (Genesis 1:1 - 23:20)
- **Images Generated**: 458 of 592
- **Chapters Done**: 1-23 of 50
- **Remaining**: 941 verses (chapters 24-50)

---

## WEB PAGES

| URL | Purpose |
|-----|---------|
| `/index.html` | Landing page with stats |
| `/visualizer.html` | Main reader with editing |
| `/gallery.html` | Grid gallery view |

---

## TROUBLESHOOTING

**API Key not working?**
```bash
python test_api_key.py
```

**Missing images?**
```bash
python batch_generate_images.py
```

**Server not starting?**
- Check if port 8003/8005 are in use
- Verify .env file exists with OPENAI_API_KEY

---

## ASCII ART CHARACTERS

Common Unicode for ASCII art:
```
Box Drawing: ═ ║ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬ ─ │ ┌ ┐ └ ┘
Stars: ✨ ⭐ ★ ☆ ✦ ✧
Nature: 🌍 🌊 🌿 🌳 🏔️ ☀️ 🌙 🌈
People: 👤 👨 👩 👴 👶 🙏
Objects: 📖 ⚡ 🔥 💧 🕊️ ⛵ 🏠
Symbols: ✝️ † ☩ ✞ ⚔️ 👑 🛡️
```

---

*Keep this file open for quick reference while working!*
