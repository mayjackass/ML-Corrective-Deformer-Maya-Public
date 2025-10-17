@echo off
echo ========================================
echo   ML Corrective Deformer - Git Setup
echo ========================================
echo.

REM Get repository URL from user
set /p REPO_URL="Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): "

echo.
echo Setting up Git repository...
echo.

REM Navigate to project directory
cd "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

REM Initialize Git if not already done
if not exist ".git" (
    echo [1/7] Initializing Git repository...
    git init
) else (
    echo [1/7] Git repository already initialized
)

REM Configure Git (optional, skip if already configured)
echo [2/7] Configuring Git...
git config user.name >nul 2>&1
if errorlevel 1 (
    set /p GIT_NAME="Enter your name: "
    set /p GIT_EMAIL="Enter your email: "
    git config --global user.name "%GIT_NAME%"
    git config --global user.email "%GIT_EMAIL%"
)

REM Add all files
echo [3/7] Adding all files...
git add .

REM Commit
echo [4/7] Creating initial commit...
git commit -m "Initial commit - ML Corrective Deformer Phase 1 complete"

REM Create main branch
echo [5/7] Setting up main branch...
git branch -M main

REM Add remote
echo [6/7] Adding remote repository...
git remote add origin %REPO_URL%

REM Push to GitHub
echo [7/7] Pushing to GitHub...
git push -u origin main

echo.
echo ========================================
echo   SUCCESS! Repository uploaded!
echo ========================================
echo.
echo Next steps:
echo 1. Go to your GitHub repository
echo 2. Click Settings -^> Pages
echo 3. Set Source to: main branch, / (root) folder
echo 4. Click Save
echo 5. Wait 2-3 minutes
echo 6. Visit your site!
echo.
pause
