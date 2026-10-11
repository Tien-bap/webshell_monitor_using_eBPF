from datetime import datetime
import socket
import struct
from monitors.base_monitor import BaseMonitor

class BindMonitor(BaseMonitor):
    def __init__(self, container_mgr, filter_mgr, logger):
        super().__init__("ebpf/bind_monitor.c", logger)
        self.container_mgr = container_mgr
        self.filter_mgr = filter_mgr

    def handle_event(self, cpu, data, size):
        event = (self.bpf["events"].event(data))
        ip = socket.inet_ntoa(struct.pack("I", event.addr))
        port = socket.ntohs(event.port)
        cgroup_id = event.cgroup

        timestamp = datetime.now().strftime("%H:%M:%S")

        if not (self.container_mgr.check_container(cgroup_id)):
            return
        
        if (self.filter_mgr.is_ignored(event.pid)):
            return
        
        container_name = (self.container_mgr.get_name(cgroup_id))
        terminal_message = f"[{timestamp}] " + f"[NET-BIND] " + f"[{container_name}] " + f"PID={event.pid} " + f"PROC={event.comm.decode()} -> {ip}:{port}"
        self.print_terminal_event(terminal_message)
        self.log_event(
            "bind",
            container_name,
            event.pid,
            event.tgid,
            event.ppid,
            event.comm.decode(),
            {
                "ip": ip,
                "port": port
            }
        )