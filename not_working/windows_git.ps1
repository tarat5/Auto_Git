param(
    [string]$RepoDir = ".",
    [string]$Branch = ""
)

# Move to the repository directory
Set-Location -Path $RepoDir

# Ensure it's a Git repository
if (-not (Test-Path "$RepoDir\.git")) {
    Write-Host "Error: The specified directory '$RepoDir' is not a Git repository."
    exit 1
}

# Get the current branch if none is specified
if (-not $Branch) {
    $Branch = git symbolic-ref --short HEAD 2>$null
    if (-not $Branch) {
        Write-Host "Error: Unable to determine the current branch. Please specify a branch."
        exit 1
    }
}

Write-Host "Fetching updates from the remote repository..."
git fetch origin

# Get commit hashes
$Local = git rev-parse HEAD
$Remote = git rev-parse origin/$Branch 2>$null
if (-not $Remote) {
    Write-Host "Error: Branch '$Branch' does not exist on the remote."
    exit 1
}
$Base = git merge-base HEAD origin/$Branch

# Compare branches
if ($Local -eq $Remote) {
    Write-Host "Local branch is up-to-date with 'origin/$Branch'."
} elseif ($Local -eq $Base) {
    Write-Host "Local branch is outdated. Run: git pull origin $Branch"
} elseif ($Remote -eq $Base) {
    Write-Host "Local branch has unpushed changes. Run: git push origin $Branch"
} else {
    Write-Host "Branches have diverged. Manual intervention required."
}

# Detect untracked (new) files
$UntrackedFiles = git ls-files --others --exclude-standard

if ($UntrackedFiles) {
    Write-Host "There are new untracked files:"
    Write-Host $UntrackedFiles
} else {
    Write-Host "No untracked files found."
}

# Restore missing files
$MissingFiles = git ls-tree -r origin/$Branch --name-only | Where-Object { -not (Test-Path $_) }

if ($MissingFiles) {
    Write-Host "Restoring missing files..."
    foreach ($file in $MissingFiles) {
        git checkout -- $file
    }
} else {
    Write-Host "No missing files found."
}

Write-Host "Git script finished successfully."
