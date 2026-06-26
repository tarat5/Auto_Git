import time
import json
import platform
import uuid
from pathlib import Path
from datetime import datetime, timezone
from git import Repo

# -----------------------------
# Returns Current Time
# -----------------------------
def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")

# -----------------------------
# Loads the tracker file 
# -----------------------------
def load_tracker_json(tracker_file):
    if not tracker_file.exists():
        return {
            "updated_at": None,
            "computers": {}
        }

    with open(tracker_file, "r", encoding="utf-8") as file:
        return json.load(file)

# -----------------------------
# Saves the tracker file 
# -----------------------------
def save_tracker_json(tracker_file, tracker_data):
    with open(tracker_file, "w", encoding="utf-8") as file:
        json.dump(tracker_data, file, indent=2)

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

#git fetch
#git log -1 --format="%ci %h %s" origin/main
#returns the latest commit but as long as commit and push are in the same time roughly it will work

def log_pull_to_json(repo_dir, pull_result, tracker_file_name="custom_git_logger.json"):
    repo_dir = Path(repo_dir)
    tracker_file = repo_dir / tracker_file_name

    tracker_data = load_tracker_json(tracker_file)

    current_time = now_iso()
    device_info = get_device_info()

    computer_id = device_info["hostname"] + "-" + device_info["hardware_id"]
    repo_key = str(repo_dir)

    if "computers" not in tracker_data:
        tracker_data["computers"] = {}

    if computer_id not in tracker_data["computers"]:
        tracker_data["computers"][computer_id] = {
            "meta": device_info,
            "repos": {}
        }

    computer_entry = tracker_data["computers"][computer_id]

    # Keep meta simple: only device identity info.
    computer_entry["meta"] = device_info

    if "repos" not in computer_entry:
        computer_entry["repos"] = {}

    if repo_key not in computer_entry["repos"]:
        computer_entry["repos"][repo_key] = {
            "repo_path": repo_key,
            "repo_name": repo_dir.name,
            "pulls": [],
            "pushes": []
        }

    repo_entry = computer_entry["repos"][repo_key]

    pull_event = {
        "time": current_time,
        "status": "success" if pull_result["success"] else "failed",
        "stdout": pull_result["stdout"],
        "stderr": pull_result["stderr"]
    }

    old_pulls = repo_entry.get("pulls", [])
    repo_entry["pulls"] = [pull_event] + old_pulls[:1]

    if "pushes" not in repo_entry:
        repo_entry["pushes"] = []

    save_tracker_json(tracker_file, tracker_data)

    return pull_event

# -----------------------------
# Turns Datetime strings into Datetime object
# -----------------------------
def parse_time(value):
    if value is None or value == "":
        return None

    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None

# -----------------------------
# Returns newest time for evetns 
# -----------------------------
def get_latest_event(events):
    """Given a list of pull or push events, return the event with the newest time."""

    if events is None or  len(events) == 0:
        return None

    latest_event = None
    latest_time = None

    for event in events:
        event_time_string = event.get("time")
        event_time = parse_time(event_time_string)

        # Skip events with missing or invalid time.
        if event_time is None:
            continue

        # First valid event found.
        if latest_time is None:
            latest_time = event_time
            latest_event = event
            continue

        # Replace latest if this event is newer.
        if event_time > latest_time:
            latest_time = event_time
            latest_event = event

    return latest_event

# -----------------------------
# Call this function as this will be the main parser
# -----------------------------
def get_git_logs(repo_dir, tracker_file_name="custom_git_logger.json"):
    """
    Reads the tracker JSON file from the repo directory.

    Returns each computer's latest pull time and latest push time.
    """

    repo_dir = Path(repo_dir)
    tracker_file = repo_dir / tracker_file_name

    if not tracker_file.exists():
        raise FileNotFoundError("Tracker file does not exist: " + str(tracker_file))

    with open(tracker_file, "r", encoding="utf-8") as file:
        tracker_data = json.load(file)

    results = {}

    computers = tracker_data.get("computers", {})

    for computer_key in computers:
        computer_data = computers[computer_key]

        computer_name = computer_data.get("computer_name", computer_key)
        repos = computer_data.get("repos", {})

        latest_pull_time = None
        latest_push_time = None

        computer_result = {
            "computer_name": computer_name,
            "repos": {},
            "latest_pull_time": None,
            "latest_push_time": None,
        }

        for repo_path in repos:
            repo_data = repos[repo_path]

            pulls = repo_data.get("pulls", [])
            pushes = repo_data.get("pushes", [])

            latest_pull = get_latest_event(pulls)
            latest_push = get_latest_event(pushes)

            if latest_pull is not None:
                pull_time_string = latest_pull.get("time")
            else:
                pull_time_string = None

            if latest_push is not None:
                push_time_string = latest_push.get("time")
            else:
                push_time_string = None

            computer_result["repos"][repo_path] = {
                "last_pull_time": pull_time_string,
                "last_push_time": push_time_string,
                "last_pull": latest_pull,
                "last_push": latest_push,
            }

            pull_time = parse_time(pull_time_string)
            push_time = parse_time(push_time_string)

            if pull_time is not None:
                if latest_pull_time is None or pull_time > latest_pull_time:
                    latest_pull_time = pull_time

            if push_time is not None:
                if latest_push_time is None or push_time > latest_push_time:
                    latest_push_time = push_time

        if latest_pull_time is not None:
            computer_result["latest_pull_time"] = latest_pull_time.isoformat()

        if latest_push_time is not None:
            computer_result["latest_push_time"] = latest_push_time.isoformat()

        results[computer_name] = computer_result

    return results