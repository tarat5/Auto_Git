import time
from pathlib import Path
from git import Repo

from get_info import get_device_info

repo = Repo(r"C:\Users\craig\Desktop\PCB_CAD")
fetch_head = Path(repo.git_dir) / "FETCH_HEAD"

should_fetch = (
    not fetch_head.exists()
    or time.time() - fetch_head.stat().st_mtime > 3600  # 1 hour
)

if should_fetch:
    repo.remotes.origin.fetch()