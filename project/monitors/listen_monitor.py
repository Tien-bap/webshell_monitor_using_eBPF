from datetime import datetime
import socket
import struct
from monitors.base_monitor import BaseMonitor

class ListenMonitor(BaseMonitor):
    def __init__(self, container_mgr, filter_mgr, logger):
        super().__init__("ebpf/listen_monitor.c", logger)
        self.container_mgr = container_mgr
        self.filter_mgr = filter_mgr

    def handle_event(self, cpu, data, size):
        event = (self.bpf["events"].event(data))
        cgroup_id = event.cgroup

        timestamp = datetime.now().strftime("%H:%M:%S")

        if not (self.container_mgr.check_container(cgroup_id)):
            return
        
        if (self.filter_mgr.is_ignored(event.pid)):
            return
        
        container_name = (self.container_mgr.get_name(cgroup_id))
        terminal_message = f"[{timestamp}] [NET-LISTEN] [{container_name}] PID={event.pid} PROC={event.comm.decode()} FD={event.fd} BACKLOG={event.backlog}"

        self.print_terminal_event(terminal_message)

        self.log_event(
            "listen",
            container_name,
            event.pid,
            event.tgid,
            event.ppid,
            event.comm.decode(),
            {
                "fd": event.fd,
                "backlog": event.backlog
            }
        )