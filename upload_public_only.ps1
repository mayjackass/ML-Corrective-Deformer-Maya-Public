# Upload Only Public Files to GitHub
# This uploads documentation and web files, excludes development files

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Uploading Public Files Only" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$repoUrl = "https://github.com/mayjackass/ML-Corrective-Deformer-Maya-Public.git"

# Navigate to project
Set-Location "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

try {
    # Initialize if needed
    if (-not (Test-Path ".git")) {
        Write-Host "[1/9] Initializing Git..." -ForegroundColor Yellow
        git init
    } else {
        Write-Host "[1/9] Git already initialized" -ForegroundColor Green
    }

    # Create main branch
    Write-Host "[2/9] Setting up main branch..." -ForegroundColor Yellow
    git branch -M main

    # Add ONLY public files
    Write-Host "[3/9] Adding public files..." -ForegroundColor Yellow
    
    # Documentation files
    git add index.html
    git add _config.yml
    git add README.md
    git add 00_START_HERE.md
    git add PROJECT_SUMMARY.md
    git add QUICK_REFERENCE.md
    git add GETTING_STARTED.md
    git add .gitignore
    git add requirements.txt
    git add config.json
    
    # Documentation folder
    git add docs/
    
    # Setup guides (useful for users)
    git add CREATE_GITHUB_REPO.md
    git add GITHUB_PAGES_SETUP.md
    git add MAKE_PUBLIC_NOW.md
    git add START_HERE_NO_REPO.md
    git add UPLOAD_NOW.md
    
    Write-Host "    Added documentation files" -ForegroundColor Green

    # Add example/reference code (read-only for users)
    Write-Host "[4/9] Adding reference code..." -ForegroundColor Yellow
    git add phase1_python_prototype/*.py
    git add ml_training/*.py
    git add utils/*.py
    
    Write-Host "    Added Python code files" -ForegroundColor Green

    # Check what's being committed
    Write-Host "[5/9] Checking files to commit..." -ForegroundColor Yellow
    $status = git status --short
    $fileCount = ($status | Measure-Object).Count
    Write-Host "    $fileCount files ready to commit" -ForegroundColor Green
    Write-Host ""
    Write-Host "Files to be uploaded:" -ForegroundColor Cyan
    git status --short | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
    Write-Host ""

    # Confirm
    $confirm = Read-Host "Continue with upload? (Y/N)"
    if ($confirm -ne "Y" -and $confirm -ne "y") {
        Write-Host "Upload cancelled." -ForegroundColor Yellow
        exit
    }

    # Commit
    Write-Host "[6/9] Creating commit..." -ForegroundColor Yellow
    git commit -m "Public release - ML Corrective Deformer documentation and code"
    Write-Host "    Commit created" -ForegroundColor Green

    # Add remote
    Write-Host "[7/9] Adding remote repository..." -ForegroundColor Yellow
    $existingRemote = git remote get-url origin 2>$null
    if ($existingRemote) {
        git remote remove origin
    }
    git remote add origin $repoUrl
    Write-Host "    Remote added" -ForegroundColor Green

    # Push
    Write-Host "[8/9] Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host "    This may take a minute..." -ForegroundColor Gray
    git push -u origin main --force

    Write-Host "[9/9] Cleaning up..." -ForegroundColor Yellow
    Write-Host "    Done!" -ForegroundColor Green

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Public files uploaded!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "Repository:" -ForegroundColor Cyan
    Write-Host "  https://github.com/mayjackass/ML-Corrective-Deformer-Maya-Public" -ForegroundColor White
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/mayjackass/ML-Corrective-Deformer-Maya-Public/settings/pages" -ForegroundColor White
    Write-Host "2. Set Source: main branch, / (root) folder" -ForegroundColor White
    Write-Host "3. Click Save" -ForegroundColor White
    Write-Host "4. Wait 2-3 minutes" -ForegroundColor White
    Write-Host "5. Visit: https://mayjackass.github.io/ML-Corrective-Deformer-Maya-Public/" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Opening GitHub in browser..." -ForegroundColor Gray
    Start-Process "https://github.com/mayjackass/ML-Corrective-Deformer-Maya-Public"

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
