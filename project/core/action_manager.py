from pathlib import Path
import json

import signal
from watchdog.observers import Observer
from core.filter_handler import FilterHandler


class ActionManager:

    def __init__(self, filter_file):
        self.filter_file = str(Path(filter_file).resolve())
        self.ignored_pids = set()


    def load(self):
        with open(self.filter_file) as f:
            data = json.load(f)

        self.ignored_pids = set(data["ignored_pids"])
    
    def ignore_pids(self, event):
        self.load()
        self.ignored_pids.add(event["pid"])
        self.save()


    def kill(self, event ):
        # Implement the logic to kill the process with the given PID
        # For example, you can use the os module to send a termination signal
        import os
        try:
            os.kill(event["pid"], signal.SIGKILL)  # Send SIGKILL signal
            print(f"Process {event['pid']} killed.")
        except ProcessLookupError:
            print(f"Process {event['pid']} not found.")
        except PermissionError:
            print(f"Permission denied to kill process {event['pid']}.")

    def save(self):
        with open(self.filter_file, "w") as f:
            json.dump(
                {
                    "ignored_pids": sorted(self.ignored_pids)
                },
                f,
                indent=4
            )
        
    