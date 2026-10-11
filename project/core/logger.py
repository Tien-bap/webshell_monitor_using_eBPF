import json
from queue import Queue
import threading
from collections import deque

class Logger:

    def __init__(self, logfile, dashboard_queue, alert_mgr, process_cache):
        self.logfile = logfile
        self.dashboard_queue = dashboard_queue
        self.alert_mgr = alert_mgr
        self.process_cache = process_cache
        self.event_id = self.load_event_id()
        self.queue = Queue()
        self.deque = deque()
        self.limit = 100
        self.pid_map = {}

    def load_event_id(self):
        try:
            with open("data/state.json") as f:
                data = json.load(f)
            
            return data["last_event_id"]
        except:
            return 0
        
    def save_event_id(self):
        with open("data/state.json", "w") as f:
            json.dump({
                "last_event_id": self.event_id
            }, f)

    def log(self, event, pid, ppid):
        self.event_id += 1
        self.pid_map[pid] = self.event_id
        parent_event_id = self.pid_map.get(ppid, -1)

        self.deque.append(pid)
        if len(self.deque) > self.limit:
            old_pid = self.deque.popleft()
            self.pid_map.pop(old_pid, None)
            
        event = {
            "event_id":self.event_id,
            "parent_event_id": parent_event_id,
            **event
        }
        self.queue.put(event)
        self.dashboard_queue.put(event)
        self.alert_mgr.add_event(event)
        self.process_cache.update_cache(event)
        self.save_event_id()

    def worker(self):
        while True:
            event = self.queue.get()
            with open(self.logfile, "a") as f:
                f.write(json.dumps(event) + "\n")

            self.queue.task_done()

    def start(self):
        threading.Thread(
            target=self.worker,
            daemon=True
        ).start()