import os
import subprocess



curdir = os.path.dirname(os.path.abspath(__file__))
#print(f"Current script is located in: {curdir}")

shell_script = os.path.join(curdir, "git.sh")
arguments = ["--repo", "/home/calEng/Desktop/Link-Outs", "main"]

result = subprocess.run(
    ["bash", shell_script] + arguments,  # Pass the arguments to the shell script
    cwd=curdir,  # Ensure the script runs in the correct directory
    text=True,  # Output as text instead of bytes
    capture_output=True,  # Capture both stdout and stderr
)

print("Shell script output:")
print(result.stdout)

if result.stderr:
    print("Shell script errors:")
    print(result.stderr)

if result.returncode == 0:
    print(f"Git bash finished")

elif result.returncode != 0:
    print(f"Error: The script returned a non-zero exit code: {result.returncode}")
    #print("Error details:")
    #print(result.stderr)

# after git add . (missing files)
# git restore --staged Physics.txt
# git restore Physics.txt
