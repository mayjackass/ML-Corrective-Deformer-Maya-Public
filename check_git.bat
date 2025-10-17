@echo off
echo ========================================
echo   GitHub Repository Setup Helper
echo ========================================
echo.

echo Checking if Git is installed...
git --version 2>nul
if %errorlevel% equ 0 (
    echo [OK] Git is installed!
    echo.
    echo You can use Option 2 in CREATE_GITHUB_REPO.md
    echo.
) else (
    echo [!] Git is NOT installed
    echo.
    echo OPTION 1: Install Git
    echo   Download from: https://git-scm.com/download/win
    echo.
    echo OPTION 2: Use GitHub Web Interface (No Git needed!)
    echo   See CREATE_GITHUB_REPO.md - Option 1
    echo.
)

echo ========================================
echo   Quick Setup (No Git Required)
echo ========================================
echo.
echo 1. Go to: https://github.com/new
echo 2. Name: ML-Corrective-Deformer-Maya
echo 3. Make it Public
echo 4. Create repository
echo 5. Upload files from this folder
echo 6. Enable Pages in Settings
echo.
echo See CREATE_GITHUB_REPO.md for detailed steps!
echo.

pause
