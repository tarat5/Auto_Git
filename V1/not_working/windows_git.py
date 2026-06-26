import os
import subprocess
import platform

# Define the repository path
path_to_repo = r"C:\Users\decla\Desktop\Link-Outs"

curdir = os.path.dirname(os.path.abspath(__file__))

shell_script = os.path.join(curdir, "windows_git.ps1")
shell_command = ["powershell", "-ExecutionPolicy", "Bypass", "-File", shell_script, "-RepoDir", path_to_repo, "-Branch", "main"]


# Run the script
result = subprocess.run(
    shell_command,
    cwd=curdir,
    text=True,
    capture_output=True
)

print("Powershell script output:\n")
print(result.stdout)

if result.stderr:
    print("Shell script errors:")
    print(result.stderr)

if result.returncode != 0:
    print(f"Error: The script returned a non-zero exit code: {result.returncode}")
