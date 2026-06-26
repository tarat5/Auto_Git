import time
from pathlib import Path
from datetime import datetime
from git import Repo

from get_info import get_device_info

# Repository location
repo_path = Path(r"C:\Users\craig\Desktop\PCB_CAD")

print("=" * 60)
print("Opening Git repository...")
print(f"Repository: {repo_path}")

repo = Repo(repo_path)

print(f"Git directory: {repo.git_dir}")

# Location of FETCH_HEAD
fetch_head = Path(repo.git_dir) / "FETCH_HEAD"

print(f"FETCH_HEAD path: {fetch_head}")

if fetch_head.exists():
    print("FETCH_HEAD exists.")

    timestamp = fetch_head.stat().st_mtime
    last_fetch = datetime.fromtimestamp(timestamp)

    print(f"Last fetch was at: {last_fetch}")

else:
    print("FETCH_HEAD does not exist.")
    last_fetch = None

# Determine if we should fetch
print("\nChecking whether a fetch is needed...")

should_fetch = (
    not fetch_head.exists()
    or time.time() - fetch_head.stat().st_mtime > 3600
)

if should_fetch:
    print("More than one hour has passed (or no previous fetch).")
    print("Fetching from origin...")

    result = repo.remotes.origin.fetch()

    print("Fetch completed!")

    for item in result:
        print(f"Updated: {item.name}")

    # Reload timestamp since FETCH_HEAD was updated
    timestamp = fetch_head.stat().st_mtime
    last_fetch = datetime.fromtimestamp(timestamp)

else:
    print("Repository was fetched less than one hour ago.")
    print("Skipping fetch.")

print("\nCurrent last fetch time:")
print(last_fetch)

# -------------------------------------------------------
# Save information to a text file
# -------------------------------------------------------

output_file = repo_path / "last_fetch.txt"

print(f"\nWriting information to:")
print(output_file)
info = get_device_info()

with open(output_file, "w") as f:
    f.write("Git Fetch Information\n")
    f.write(f"OS         : {info[0]}\n")
    f.write(f"Hardware ID: {info[1]}\n")
    f.write("====================\n")
    f.write(f"Repository : {repo_path}\n")
    f.write(f"Checked At : {datetime.now()}\n")
    f.write(f"Last Fetch : {last_fetch}\n")
    f.write(f"Fetched Now: {'Yes' if should_fetch else 'No'}\n")


print("Finished writing file.")

print("=" * 60)
print("Done.")