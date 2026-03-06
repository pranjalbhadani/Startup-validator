# Creates folder structure for Startup Validator project
# Run this script from the root of the repository

$folders = @(
"backend",
"backend/agents",
"frontend",
"frontend/components",
"data",
"data/datasets",
"startup_vectordb",
"tests"
)

$files = @(
"backend/main.py",
"backend/models.py",
"backend/llm_service.py",
"backend/scoring.py",

"backend/agents/idea_agent.py",
"backend/agents/market_agent.py",
"backend/agents/competitor_agent.py",
"backend/agents/risk_agent.py",

"frontend/app.py",
"frontend/components/input_form.py",
"frontend/components/score_display.py",
"frontend/components/swot_display.py",

"data/datasets/.gitkeep",

"tests/test_api.py",

".env",
"requirements.txt",
"README.md"
)

Write-Host "`nCreating folders..."

foreach ($folder in $folders) {
    if (!(Test-Path $folder)) {
        New-Item -ItemType Directory -Path $folder | Out-Null
        Write-Host "Created folder: $folder"
    }
}

Write-Host "`nCreating files..."

foreach ($file in $files) {
    if (!(Test-Path $file)) {
        New-Item -ItemType File -Path $file | Out-Null
        Write-Host "Created file: $file"
    }
}

Write-Host "`nProject structure successfully created."