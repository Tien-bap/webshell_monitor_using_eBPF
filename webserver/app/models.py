import subprocess
from os import system

def execute_command(command):
    print(f"Executing command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        return result.stdout + result.stderr

    except Exception as e:
        return str(e)