import os
import signal

pid = int(input("pid kill: "))
os.kill(pid, signal.SIGKILL)