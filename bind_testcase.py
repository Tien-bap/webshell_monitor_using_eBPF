# bind_test.py
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 4444))

print("bind success")

time.sleep(300)
