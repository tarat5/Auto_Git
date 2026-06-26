#!/bin/bash

# Function to print usage
usage() {
    echo "Usage: $0 [--repo <path>] [branch]"
    echo "Options:"
    echo "  --repo <path>  Specify the path to the Git repository. Defaults to the current directory."
    echo "  branch         Specify the branch to compare with. Defaults to the current branch's upstream."
    exit 1
}

# Parse arguments
REPO_DIR="."
TARGET_BRANCH=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --repo)
            REPO_DIR=$2
            shift 2
            ;;
        *)
            TARGET_BRANCH=$1
            shift
            ;;
    esac
done

# Ensure the specified directory is a Git repository
if ! (cd "$REPO_DIR" && git rev-parse --is-inside-work-tree) &> /dev/null; then
    echo "The specified directory '$REPO_DIR' is not a Git repository. Please provide a valid Git repository."
    exit 1
fi

# Move to the specified repository directory
cd "$REPO_DIR" || exit

# Get the current branch if no branch is specified
if [ -z "$TARGET_BRANCH" ]; then
    TARGET_BRANCH=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
    if [ -z "$TARGET_BRANCH" ]; then
        echo "No branch specified and no upstream branch set. Please specify a branch or set an upstream branch."
        usage
    fi
fi

# Fetch updates from the remote repository
echo "Fetching updates from the remote repository for branch '$TARGET_BRANCH'..."
git fetch origin

# Compare the local branch with the target branch
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "$TARGET_BRANCH" 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "The branch '$TARGET_BRANCH' does not exist. Please check the branch name and try again."
    exit 1
fi
BASE=$(git merge-base HEAD "$TARGET_BRANCH")

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "The local branch is up-to-date with the remote branch '$TARGET_BRANCH'."
elif [ "$LOCAL" = "$BASE" ]; then
    echo "The local branch is outdated compared to '$TARGET_BRANCH'. Pull the latest changes using 'git pull origin $TARGET_BRANCH'."
elif [ "$REMOTE" = "$BASE" ]; then
    echo "The local branch has changes that are not pushed to '$TARGET_BRANCH'. Push your changes using 'git push origin $(git rev-parse --abbrev-ref HEAD)'."
else
    echo "The local and remote branches have diverged. Manual intervention is required."
fi

# Check for untracked files (new files not yet added to git)
UNTRACKED_FILES=$(git ls-files --others --exclude-standard)
if [ -n "$UNTRACKED_FILES" ]; then
    echo "There are untracked files in the repository:"
    echo "$UNTRACKED_FILES"
else
    echo "No untracked files found."
fi

# Check for staged but uncommitted files
STAGED_FILES=$(git diff --cached --name-only)
if [ -n "$STAGED_FILES" ]; then
    echo "There are staged but uncommitted files:"
    echo "$STAGED_FILES"
else
    echo "No staged but uncommitted files found."
fi

# Check for deleted files (files that are removed locally but tracked by Git)
DELETED_FILES=$(git status --porcelain | grep '^ D' | sed 's/^ D //')

if [ -n "$DELETED_FILES" ]; then
    echo "The following files have been deleted locally but are still tracked by Git:"
    echo "$DELETED_FILES"
else
    echo "No deleted files found."
fi

# Get the list of files in the remote repository at the target branch
REMOTE_FILES=$(git ls-tree -r "$TARGET_BRANCH" --name-only)

# Get the list of files that are tracked in the local repository
LOCAL_FILES=$(git ls-files)

# Compare the lists using comm, ensuring they are sorted
MISSING_FILES=$(comm -23 <(echo "$REMOTE_FILES" | sort) <(echo "$LOCAL_FILES" | sort))

if [ -n "$MISSING_FILES" ]; then
    echo "The following files are missing in the local repository but exist in the remote repository:"
    echo "$MISSING_FILES"
else
    echo "No missing files found."
fi
