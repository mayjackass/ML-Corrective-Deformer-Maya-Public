# ML Corrective Deformer - Automated GitHub Setup
# Run this script to upload everything to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ML Corrective Deformer - Git Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get repository URL
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "Error: Repository URL is required!" -ForegroundColor Red
    pause
    exit
}

Write-Host ""
Write-Host "Setting up Git repository..." -ForegroundColor Green
Write-Host ""

# Navigate to project directory
Set-Location "C:\Users\Burn\Documents\maya\scripts\ML_deformerTool"

try {
    # Step 1: Initialize Git
    if (-not (Test-Path ".git")) {
        Write-Host "[1/8] Initializing Git repository..." -ForegroundColor Yellow
        git init
    } else {
        Write-Host "[1/8] Git repository already initialized" -ForegroundColor Green
    }

    # Step 2: Configure Git
    Write-Host "[2/8] Configuring Git..." -ForegroundColor Yellow
    $userName = git config user.name
    if ([string]::IsNullOrWhiteSpace($userName)) {
        $gitName = Read-Host "Enter your name for Git"
        $gitEmail = Read-Host "Enter your email for Git"
        git config --global user.name "$gitName"
        git config --global user.email "$gitEmail"
    } else {
        Write-Host "    Using existing Git config: $userName" -ForegroundColor Gray
    }

    # Step 3: Add all files
    Write-Host "[3/8] Adding all files..." -ForegroundColor Yellow
    git add .
    Write-Host "    Added all files" -ForegroundColor Green

    # Step 4: Check status
    Write-Host "[4/8] Checking status..." -ForegroundColor Yellow
    $status = git status --short
    $fileCount = ($status | Measure-Object).Count
    Write-Host "    $fileCount files ready to commit" -ForegroundColor Green

    # Step 5: Commit
    Write-Host "[5/8] Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit - ML Corrective Deformer Phase 1 complete"
    Write-Host "    Commit created successfully" -ForegroundColor Green

    # Step 6: Create main branch
    Write-Host "[6/8] Setting up main branch..." -ForegroundColor Yellow
    git branch -M main
    Write-Host "    Main branch ready" -ForegroundColor Green

    # Step 7: Add remote
    Write-Host "[7/8] Adding remote repository..." -ForegroundColor Yellow
    
    # Check if remote already exists
    $existingRemote = git remote get-url origin 2>$null
    if ($existingRemote) {
        Write-Host "    Removing existing remote..." -ForegroundColor Gray
        git remote remove origin
    }
    
    git remote add origin $repoUrl
    Write-Host "    Remote added: $repoUrl" -ForegroundColor Green

    # Step 8: Push to GitHub
    Write-Host "[8/8] Pushing to GitHub..." -ForegroundColor Yellow
    Write-Host "    This may take a minute..." -ForegroundColor Gray
    git push -u origin main

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  SUCCESS! Repository uploaded!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Extract repo info
    $repoUrl -match "github\.com[:/]([^/]+)/([^/\.]+)" | Out-Null
    $username = $matches[1]
    $repoName = $matches[2]
    
    Write-Host "Your repository is now live at:" -ForegroundColor Cyan
    Write-Host "  https://github.com/$username/$repoName" -ForegroundColor White
    Write-Host ""
    Write-Host "NEXT STEPS:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/$username/$repoName/settings/pages" -ForegroundColor White
    Write-Host "2. Under 'Source', select: main branch, / (root) folder" -ForegroundColor White
    Write-Host "3. Click 'Save'" -ForegroundColor White
    Write-Host "4. Wait 2-3 minutes for deployment" -ForegroundColor White
    Write-Host "5. Visit your site at: https://$username.github.io/$repoName/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Opening GitHub repository in browser..." -ForegroundColor Gray
    Start-Process "https://github.com/$username/$repoName"
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "- Make sure the repository URL is correct" -ForegroundColor White
    Write-Host "- Check if the repository already exists on GitHub" -ForegroundColor White
    Write-Host "- Verify you have permission to push to this repository" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
