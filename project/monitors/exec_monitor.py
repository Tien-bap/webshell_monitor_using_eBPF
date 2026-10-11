from monitors.base_monitor import BaseMonitor
from datetime import datetime
import os

class ExecMonitor(BaseMonitor):
    def __init__(self, container_mgr, filter_mgr, logger):
        super().__init__("ebpf/exec_monitor.c", logger)
        self.container_mgr = container_mgr
        self.filter_mgr = filter_mgr

    def get_cmdline(self, pid):
        try: 
            with open(f"/proc/{pid}/cmdline", "rb") as f:
                return f.read().replace(b"\x00", b" ").decode(errors="ignore").strip()
        except:
            return ""

    def handle_event(self, cpu, data, size):
        event = (self.bpf["events"].event(data))

        timestamp = (datetime.now().strftime("%H:%M:%S"))
        cgroup_id = event.cgroup_id

        if not (self.container_mgr.check_container(cgroup_id)):
            return
        
        container_name = self.container_mgr.get_name(cgroup_id)

        if self.filter_mgr.is_ignored(event.pid):
            return


        arg1 = event.cmd_args1.decode(errors="ignore").strip("\x00")
        arg2 = event.cmd_args2.decode(errors="ignore").strip("\x00")
        arg3 = event.cmd_args3.decode(errors="ignore").strip("\x00")
        arg4 = event.cmd_args4.decode(errors="ignore").strip("\x00")
        arg5 = event.cmd_args5.decode(errors="ignore").strip("\x00")
        cmdline = event.filename.decode(errors="ignore").strip("\x00")
        cmd = f"{cmdline} {arg1} {arg2} {arg3} {arg4} {arg5}".strip()

        args = [
            arg1,
            arg2,
            arg3,
            arg4,
            arg5
        ]
    
        command = self.extract_command(cmdline, args)

        terminal_message = f"[{timestamp}] "+ f"[EXECVE] [{container_name}] " + f"PID={event.pid} " + f"TGID={event.tgid} " + f"PPID={event.ppid} " + f"PROC={event.comm.decode()} " + f"CMD={cmd}"

        self.print_terminal_event(terminal_message)

        self.log_event(
            "execve",
            container_name,
            event.pid,
            event.tgid,
            event.ppid,
            event.comm.decode(),
            {
                "cmd_full": cmd,
                "command": command
            }
        )

    
    def extract_command(self, filename, args):
        executable = os.path.basename(filename)
        
        args = [a for a in args if a]

        # sh -c / bash -c
        if executable in ("sh", "bash"):

            i = 0

            while i < len(args) and args[i].startswith("-"):
                i += 1

            if i >= len(args):
                return executable

            return args[i]

        # Execve bình thường
        return executable






    