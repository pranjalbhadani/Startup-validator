# ==========================================
# Startup Validator Project Structure Setup
# ==========================================

$root = "startup-validator"

$folders = @(
    "$root",
    "$root\MVP",
    "$root\MVP\agents"
)

$files = @(
    "$root\MVP\agents\idea_agent.py",
    "$root\MVP\agents\market_agent.py",
    "$root\MVP\agents\competitor_agent.py",
    "$root\MVP\agents\risk_agent.py",
    "$root\MVP\pipeline.py",
    "$root\MVP\main.py",
    "$root\MVP\scoring.py",
    "$root\MVP\models.py",
    "$root\MVP\llm_service.py",
    "$root\MVP\app.py",
    "$root\MVP\requirements.txt"
)

Write-Host "`nChecking folders..."

foreach ($folder in $folders) {

    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created folder: $folder"
    }
    else {
        Write-Host "Exists: $folder"
    }
}

Write-Host "`nChecking files..."

foreach ($file in $files) {

    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "Created file: $file"
    }
    else {
        Write-Host "Exists: $file"
    }
}

Write-Host "`nProject structure verification complete."