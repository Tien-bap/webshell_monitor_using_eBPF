from bcc import BPF
from datetime import datetime

class BaseMonitor:

    def __init__(self, bpf_file, logger):
        self.bpf = BPF(src_file=bpf_file)
        self.logger = logger

    def start(self):
        self.bpf["events"].open_perf_buffer(self.handle_event)

    def poll(self):
        while True:
            self.bpf.perf_buffer_poll()

    def handle_event(self, cpu, data, size):
        raise NotImplementedError
    
    def log_event(self, event_type, container_name, pid, tgid, ppid, process, detail):
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "container": container_name,
            
            "pid": pid,
            "tgid": tgid,
            "ppid": ppid,

            "process": process,
            "details": detail
        }
        
        self.logger.log(event_data, pid, ppid)


    def print_terminal_event(self, event):
        print(event)