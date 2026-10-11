from pathlib import Path
import json

from watchdog.observers import Observer
from core.filter_handler import FilterHandler


class FilterManager:

    def __init__(self, filter_file):

        self.filter_file = str(Path(filter_file).resolve())

        self.ignored_pids = set()

        self.load()

        self.observer = Observer()

        self.observer.schedule(
            FilterHandler(self),
            path=str(Path(self.filter_file).parent),
            recursive=False
        )
    def load(self):
        try:
            with open(self.filter_file) as f:
                data = json.load(f)

            self.ignored_pids = set(data["ignored_pids"])

        except json.JSONDecodeError:
            return

    def start(self):
        self.observer.start()

    def is_ignored(self, pid):
        return pid in self.ignored_pids
    
    def add_pid(self, pid):
        if pid not in self.ignored_pids:
            self.ignored_pids.add(pid)
            self.save()

    def remove_pid(self, pid):
        if pid in self.ignored_pids:
            self.ignored_pids.remove(pid)
            self.save()

    def kill(self, pid):
        # Implement the logic to kill the process with the given PID
        # For example, you can use the os module to send a termination signal
        import os
        try:
            os.kill(pid, 9)  # Send SIGKILL signal
            print(f"Process {pid} killed.")
        except ProcessLookupError:
            print(f"Process {pid} not found.")
        except PermissionError:
            print(f"Permission denied to kill process {pid}.")

    def reset(self):
        self.ignored_pids.clear()
        self.save()

    def save(self):
        with open(self.filter_file, "w") as f:
            json.dump(
                {
                    "ignored_pids": sorted(self.ignored_pids)
                },
                f,
                indent=4
            )
        
    