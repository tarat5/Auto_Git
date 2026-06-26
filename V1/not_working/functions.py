import os

def init_os():
    """returns the physical operating name"""
    if os.name == 'posix':
        return "linux"
    elif os.name == 'nt':
        return "windows"