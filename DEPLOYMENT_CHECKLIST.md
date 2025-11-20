# 🚀 Genesis Visualized - Deployment Checklist

## ✅ Pre-Deployment Checklist

### Step 1: Create Clean Deployment Folder
- [ ] Create a new folder called `genesis-visualized-web`
- [ ] Copy ONLY the files listed below (not the entire project folder)

### Step 2: Files to Include (Copy these)

**HTML Files (Required):**
- [ ] `index.html` - Homepage
- [ ] `reader.html` - Sequential verse reader
- [ ] `gallery.html` - Gallery view

**Data Files (Required):**
- [ ] `frames-database.json` - All verse data

**Image Folder (Required):**
- [ ] `images/` folder - Contains all 267+ HD images
  - Make sure it's the `images` folder, NOT `images - Copy`

**Optional but Recommended:**
- [ ] `README.md` - Project description
- [ ] `favicon.ico` - Website icon (if you want to add one)

### Step 3: Files to EXCLUDE (Do NOT upload)

**Python Development Files:**
- ❌ All `.py` files (add_verse.py, batch_generate_images.py, etc.)
- ❌ `__pycache__/` folder
- ❌ `requirements.txt`
- ❌ `verse-data.json`

**Old/Unused HTML Files:**
- ❌ `bible-visualizer.html` (old version)
- ❌ `chapters.html` (old version)
- ❌ `gallery-view.html` (old version)
- ❌ `HOME_PAGE.html` (old version)
- ❌ `visualizer.html` (duplicate of index.html)

**Test & Development Files:**
- ❌ `test_sync.txt`
- ❌ `test_file_location.txt`
- ❌ `test_api_key.py`
- ❌ `temp_add_verse.py`
- ❌ `start_server.bat`
- ❌ `nul`
- ❌ `SETUP_INSTRUCTIONS.md`
- ❌ `images - Copy/` folder

**Duplicate Folders:**
- ❌ `images\ - Copy` (backup folder, not needed)

---

## 🌐 Netlify Deployment Steps

### Step 1: Prepare Your Files
1. Create folder: `genesis-visualized-web`
2. Copy only the required files (see list above)
3. Verify `images/` folder has all PNG files

### Step 2: Deploy to Netlify
1. Go to [app.netlify.com](https://app.netlify.com)
2. Sign up (free account)
3. Drag and drop `genesis-visualized-web` folder
4. Wait 30-60 seconds

### Step 3: Configure Your Site
1. Click "Site settings"
2. Change site name to something memorable:
   - Example: `genesisvisualized.netlify.app`
3. Test all pages work:
   - [ ] Homepage loads
   - [ ] Reader works (Previous/Next buttons)
   - [ ] Gallery works (chapter filters)
   - [ ] Images display properly
   - [ ] Downloads work

### Step 4: Optional - Custom Domain
1. Buy domain (e.g., `genesisvisualized.com`) from Namecheap or Google Domains (~$12/year)
2. In Netlify: Domain settings → Add custom domain
3. Update DNS records as instructed
4. Wait 24-48 hours for DNS propagation

---

## 📊 Final Verification

Test these features on the live site:

- [ ] Homepage displays correct stats
- [ ] "Start Reading" button works
- [ ] "Browse Gallery" button works
- [ ] Reader Previous/Next navigation works
- [ ] Chapter filter buttons work
- [ ] All images load properly
- [ ] Download Image button works
- [ ] Download Full Frame button works (includes embedded image)
- [ ] All navigation links work
- [ ] Mobile responsive (test on phone)

---

## 🎯 Quick Summary

**What to upload:**
```
genesis-visualized-web/
├── index.html
├── reader.html
├── gallery.html
├── frames-database.json
├── images/
│   ├── frame_001.png
│   ├── frame_002.png
│   └── ... (all 267+ images)
└── README.md (optional)
```

**Where to upload:** [app.netlify.com](https://app.netlify.com)

**Cost:** FREE forever, no ads

**Time:** 5 minutes

---

## ✝️ To God Be The Glory

This project is offered freely to all who seek to explore God's Word.
No ads, no subscriptions, no cost.
