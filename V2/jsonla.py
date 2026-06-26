import time
import json
import platform
import uuid
from pathlib import Path
from datetime import datetime
from git import Repo


# -----------------------------
# Device Info
# -----------------------------
def get_device_info():
    os_name = f"{platform.system()} {platform.release()}"
    hostname = platform.node()
    hardware_id = hex(uuid.getnode())

    return {
        "os": os_name,
        "hostname": hostname,
        "hardware_id": hardware_id
    }


# -----------------------------
# Main Git Check Function
# -----------------------------
def run_git_fetch_tracker(repo_path_str):
    repo_path = Path(repo_path_str)

    print("=" * 60)
    print("Starting Git Fetch Tracker")
    print(f"Repository: {repo_path}")

    repo = Repo(repo_path)
    print(f"Git directory: {repo.git_dir}")

    fetch_head = Path(repo.git_dir) / "FETCH_HEAD"
    print(f"FETCH_HEAD path: {fetch_head}")

    last_fetch = None

    # -----------------------------
    # Read last fetch time
    # -----------------------------
    if fetch_head.exists():
        timestamp = fetch_head.stat().st_mtime
        last_fetch = datetime.fromtimestamp(timestamp)
        print(f"Last fetch time: {last_fetch}")
    else:
        print("No FETCH_HEAD found yet.")

    # -----------------------------
    # Decide whether to fetch
    # -----------------------------
    print("\nChecking if fetch is needed...")

    should_fetch = (
        not fetch_head.exists()
        or time.time() - fetch_head.stat().st_mtime > 3600
    )

    if should_fetch:
        print("Fetch required -> running git fetch...")

        result = repo.remotes.origin.fetch()

        print("Fetch complete!")

        for item in result:
            print(f"Updated: {item.name}")

        # update timestamp
        if fetch_head.exists():
            last_fetch = datetime.fromtimestamp(fetch_head.stat().st_mtime)

    else:
        print("Fetch not needed (less than 1 hour old).")

    # -----------------------------
    # Device info
    # -----------------------------
    info = get_device_info()

    print("\nDevice Info:")
    print(info)

    # -----------------------------
    # Save per-device log file
    # -----------------------------
    safe_device_name = info["hostname"].replace(" ", "_")
    output_file = repo_path / f"{safe_device_name}_git_log.json"

    data = {
        "device": info,
        "repository": str(repo_path),
        "checked_at": datetime.now().isoformat(),
        "last_fetch": last_fetch.isoformat() if last_fetch else None,
        "fetch_ran": should_fetch
    }

    print(f"\nWriting log file: {output_file}")

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Log written successfully.")
    print("=" * 60)


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    run_git_fetch_tracker(r"C:\Users\craig\Desktop\Auto_git")

    # C:\Users\craig\Desktop\PCB_CAD