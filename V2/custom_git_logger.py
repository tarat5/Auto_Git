import subprocess
import json
import os

#get host name and save the acquired repos accordingly 

from functions import *

custom_git_logger_dir = os.path.dirname(os.path.abspath(__file__))

list_of_repos = os.path.join(custom_git_logger_dir, "repos.json")

with open(list_of_repos, "r", encoding="utf-8") as file:
    repos = json.load(file)

for repo_num, repo_path in repos.items():
    success, output = git_fetch(repo_path)

    if(success):
        print("fetch good")
    else:
        print("fetch bad")

    # need to read the json stored in the directory

    # then compare all the push times from each computer alongside fetch time

    # if fetch or push from another computer is later than current time, pull
