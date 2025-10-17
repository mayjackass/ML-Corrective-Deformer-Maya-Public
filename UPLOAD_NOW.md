# 🚀 UPLOAD TO GITHUB - COMPLETE GUIDE

## You Have Two Options:

---

## ✅ OPTION 1: Automated Script (Recommended)

### Run the PowerShell Script:

1. **Right-click** on `setup_github.ps1`
2. Select **"Run with PowerShell"**
3. Enter your repository URL when asked
4. Follow the prompts

**OR** run from command line:
```powershell
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"
powershell -ExecutionPolicy Bypass -File setup_github.ps1
```

---

## ✅ OPTION 2: Manual Commands

### Step-by-Step (Copy and paste each command):

```powershell
# Navigate to project
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

# Initialize Git
git init

# Configure Git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Commit
git commit -m "Initial commit - ML Corrective Deformer Phase 1"

# Set branch to main
git branch -M main

# Add your repository (REPLACE with your actual URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

---

## 📋 What You Need:

### Your GitHub Repository URL

It looks like one of these:
```
https://github.com/mayjackass/ML-Corrective-Deformer-Maya.git
https://github.com/mayjackass/pose-based-corrective.git
git@github.com:mayjackass/your-repo-name.git
```

**Where to find it:**
1. Go to your repository on GitHub
2. Click the green **"Code"** button
3. Copy the HTTPS URL

---

## ⚡ FASTEST: Tell Me Your Repo URL

**Just paste your repository URL here and I'll give you the exact commands to run!**

Example format:
```
https://github.com/mayjackass/YOUR-REPO-NAME.git
```

---

## 🔧 After Upload - Enable GitHub Pages

Once files are uploaded:

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Scroll down to **Pages** (left sidebar)
4. Under **"Source"**:
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **"Save"**
6. Wait 2-3 minutes
7. Visit: `https://mayjackass.github.io/YOUR-REPO-NAME/`

---

## 🆘 Troubleshooting

### "Permission denied"
You need to authenticate with GitHub. Options:
1. Use HTTPS and enter GitHub username/password
2. Set up SSH keys
3. Use GitHub Personal Access Token

### "Remote already exists"
```powershell
git remote remove origin
git remote add origin YOUR_URL
git push -u origin main
```

### "Nothing to commit"
```powershell
git add .
git commit -m "Initial commit"
git push
```

---

## 📱 Quick Test

Check if Git is working:
```powershell
git --version
git status
```

Should show:
- Git version number
- List of files ready to commit

---

## ✅ After Upload Checklist

- [ ] Files uploaded to GitHub
- [ ] Repository is Public
- [ ] GitHub Pages enabled
- [ ] Waited 3 minutes for deployment
- [ ] Visited your site URL
- [ ] Site loads correctly
- [ ] Shared the link! 🎉

---

## 🎯 Your Final URLs Will Be:

**Repository:**
```
https://github.com/mayjackass/YOUR-REPO-NAME
```

**Public Website:**
```
https://mayjackass.github.io/YOUR-REPO-NAME/
```

**Download:**
```
https://github.com/mayjackass/YOUR-REPO-NAME/archive/refs/heads/main.zip
```

---

**Ready to upload? Pick Option 1 or 2 above, or tell me your repo URL!**
