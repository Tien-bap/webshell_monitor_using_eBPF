from monitors.base_monitor import BaseMonitor
from datetime import datetime

class OpenMonitor(BaseMonitor):
    def __init__(self, container_mgr, filter_mgr, logger):
        super().__init__("ebpf/openat_monitor.c", logger)
        self.container_mgr = container_mgr
        self.filter_mgr = filter_mgr
        

    def handle_event(self, cpu, data, size):
        event = (self.bpf["events"].event(data))
        timestamp = (datetime.now().strftime("%H:%M:%S"))

        cgroup_id = event.cgroup
        process = event.comm.decode()

        filename = event.filename.decode(errors='ignore').strip(chr(0))
        if not (self.container_mgr.check_container(cgroup_id)):
            return
        
        if (self.filter_mgr.is_ignored(event.pid)):
            return
        
        if (self.filter_mgr.is_ignored(event.pid)):
            return
        

        container_name = self.container_mgr.get_name(cgroup_id)
        terminal_message = f"[{timestamp}] " + f"[OPENAT] " + f"[{container_name}] " + f"PID={event.pid} " + f"PPID={event.ppid} " + f"PROC={process} " + f"FILE={filename}"
        self.print_terminal_event(terminal_message)

        self.log_event(
            "openat",
            container_name,
            event.pid,
            event.tgid,
            event.ppid,
            event.comm.decode(),
            filename
        )

