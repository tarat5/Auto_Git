import subprocess
from functions import *
prefix = init_os()
action = input("Type 1 to autocommit with message, 2 to check for out of date")

if action == "2":
    subprocess.run(f"python {prefix}_git.py", shell=True)