import os

def init_os():
    if os.name == 'posix':
        return "linux"
    elif os.name == 'nt':
        return "windows"