# 🚀 GitHub Repository Setup - Step by Step

## OPTION 1: Using GitHub Web Interface (Easiest - 5 minutes)

### Step 1: Create Repository on GitHub

1. **Go to GitHub**: https://github.com/new
   - Or click the **+** icon (top right) → "New repository"

2. **Fill in Repository Details**:
   - **Repository name**: `ML-Corrective-Deformer-Maya`
   - **Description**: `Pose-Based Corrective Blendshape Prediction Using Machine Learning in Maya`
   - **Visibility**: ✅ **Public** (so non-GitHub users can see it)
   - **Initialize**: ❌ Don't check any boxes (we have files already)
   - Click **"Create repository"**

3. **You'll see instructions** - ignore them for now, follow steps below

### Step 2: Upload Your Project

After creating the repo, you'll see an empty repository page.

**Two ways to upload:**

#### Method A: Upload via Web (No Git Required)

1. On the empty repo page, click **"uploading an existing file"** link
2. **Drag and drop ALL files** from: `C:\Users\Burn\Documents\maya\scripts\ML_deformerTool`
3. Scroll down, add commit message: `Initial commit - Phase 1 complete`
4. Click **"Commit changes"**

#### Method B: Upload via PowerShell (If you have Git)

```powershell
# Navigate to your project
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Phase 1 complete"

# Add your GitHub repo as remote
git branch -M main
git remote add origin https://github.com/mayjackass/ML-Corrective-Deformer-Maya.git

# Push to GitHub
git push -u origin main
```

### Step 3: Enable GitHub Pages

1. Go to your repo: `https://github.com/mayjackass/ML-Corrective-Deformer-Maya`
2. Click **"Settings"** tab (top right)
3. Scroll down left sidebar → Click **"Pages"**
4. Under **"Source"**:
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **"Save"**
6. **Wait 2-3 minutes** for deployment

### Step 4: Get Your Public URL

Your project will be live at:
```
https://mayjackass.github.io/ML-Corrective-Deformer-Maya/
```

**Check deployment status**:
- Go to **"Actions"** tab in your repo
- You'll see a workflow running
- When it's green ✅, your site is live!

---

## OPTION 2: Using Git (If Git is Installed)

### Check if Git is Installed

```powershell
git --version
```

If not installed, download from: https://git-scm.com/download/win

### Complete Setup Commands

```powershell
# 1. Navigate to project
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

# 2. Initialize Git
git init

# 3. Configure Git (first time only)
git config --global user.name "Mayj Amilano"
git config --global user.email "your-email@example.com"

# 4. Add all files
git add .

# 5. Commit
git commit -m "Initial commit - ML Corrective Deformer Phase 1 complete"

# 6. Create main branch
git branch -M main

# 7. Add GitHub remote (create repo first on GitHub.com)
git remote add origin https://github.com/mayjackass/ML-Corrective-Deformer-Maya.git

# 8. Push to GitHub
git push -u origin main
```

---

## OPTION 3: Using GitHub Desktop (Visual, Easy)

### Download and Install

1. Download: https://desktop.github.com/
2. Install and sign in to GitHub
3. Follow these steps:

### Steps in GitHub Desktop

1. **Add Repository**
   - File → Add Local Repository
   - Choose: `C:\Users\Burn\Documents\maya\scripts\ML_deformerTool`
   - Click "Create a repository here instead" (if prompted)

2. **Initial Commit**
   - Check all files in left panel
   - Summary: "Initial commit - Phase 1 complete"
   - Click "Commit to main"

3. **Publish to GitHub**
   - Click "Publish repository" (top right)
   - Name: `ML-Corrective-Deformer-Maya`
   - Description: "Pose-Based Corrective Blendshape Prediction Using Machine Learning"
   - ✅ Keep code **public**
   - Click "Publish Repository"

4. **Enable GitHub Pages**
   - Click "View on GitHub"
   - Follow Step 3 from Option 1 above

---

## 🎯 RECOMMENDED: Quick Start (Option 1 + Web Upload)

**This is the FASTEST method if you don't have Git:**

1. ✅ Go to: https://github.com/new
2. ✅ Name: `ML-Corrective-Deformer-Maya`
3. ✅ Make it **Public**
4. ✅ Create repository
5. ✅ Click "uploading an existing file"
6. ✅ Drag all files from: `C:\Users\Burn\Documents\maya\scripts\ML_deformerTool`
7. ✅ Commit changes
8. ✅ Settings → Pages → Enable (main branch, root folder)
9. ✅ Wait 2-3 minutes
10. ✅ Visit: `https://mayjackass.github.io/ML-Corrective-Deformer-Maya/`

**DONE!** 🎉

---

## 📋 Files You Should Upload

Make sure these are included:

### Essential Files
- ✅ `index.html` (your landing page)
- ✅ `_config.yml` (GitHub Pages config)
- ✅ `README.md` (main documentation)
- ✅ `00_START_HERE.md`
- ✅ `GETTING_STARTED.md`
- ✅ `QUICK_REFERENCE.md`
- ✅ `PROJECT_SUMMARY.md`

### Code Files
- ✅ `phase1_python_prototype/` (all files)
- ✅ `ml_training/` (model.py, train.py)
- ✅ `utils/` (data_collector.py)
- ✅ `docs/` (all documentation)
- ✅ `tests/` (test_basic.py)

### Configuration
- ✅ `config.json`
- ✅ `requirements.txt`
- ✅ `.gitignore`

### Optional (can exclude)
- ❌ `data/` folder (usually excluded - add to .gitignore)
- ❌ `models/` folder (large files - add to .gitignore)
- ❌ `__pycache__/` (auto-generated)

---

## 🔒 Important: .gitignore

Your `.gitignore` is already set up to exclude:
- Training data (too large)
- Trained models (too large)
- Python cache files
- Temporary files

This keeps your repo clean and fast!

---

## ✅ Verification Checklist

After setup, verify:

1. **Repository is Public**
   - Go to: `https://github.com/mayjackass/ML-Corrective-Deformer-Maya`
   - Can you see it without logging in? ✅

2. **Files are Uploaded**
   - Check main page shows all folders
   - README.md displays automatically ✅

3. **GitHub Pages is Enabled**
   - Settings → Pages shows deployment URL
   - Green checkmark in Actions tab ✅

4. **Website is Live**
   - Visit: `https://mayjackass.github.io/ML-Corrective-Deformer-Maya/`
   - Landing page loads correctly ✅

---

## 🌐 Your Final URLs

### Public Website (Anyone can access)
```
https://mayjackass.github.io/ML-Corrective-Deformer-Maya/
```

### GitHub Repository (Developers)
```
https://github.com/mayjackass/ML-Corrective-Deformer-Maya
```

### Direct Documentation Links
```
https://github.com/mayjackass/ML-Corrective-Deformer-Maya/blob/main/README.md
https://github.com/mayjackass/ML-Corrective-Deformer-Maya/blob/main/docs/QUICKSTART.md
https://github.com/mayjackass/ML-Corrective-Deformer-Maya/blob/main/docs/ARCHITECTURE.md
```

### Download Project
```
https://github.com/mayjackass/ML-Corrective-Deformer-Maya/archive/refs/heads/main.zip
```

---

## 🆘 Troubleshooting

### "Repository already exists"
- Choose a different name
- Or delete existing repo: Settings → Danger Zone → Delete

### "Upload too large"
- Files might be too big (>100MB each)
- Remove `data/` and `models/` folders
- Upload via Git LFS for large files

### "Pages not deploying"
- Check Actions tab for errors
- Make sure `index.html` is in root folder
- Wait 5 minutes and try again

### Need Help?
- GitHub Help: https://docs.github.com/en/pages
- Check Actions tab for build errors
- Try Netlify as alternative (drag & drop)

---

## 🎉 YOU'RE DONE!

Once you complete any of the options above:

1. ✅ Your project is on GitHub
2. ✅ Public website is live
3. ✅ Anyone can view documentation
4. ✅ Developers can clone/fork

**Share your link with the world!** 🚀

```
🌐 Live Website: https://mayjackass.github.io/ML-Corrective-Deformer-Maya/
📂 Source Code: https://github.com/mayjackass/ML-Corrective-Deformer-Maya
```

---

**Need help with any step? Let me know!**
