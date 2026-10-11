import socket
import time

s = socket.socket()

s.bind(("0.0.0.0", 4444))
s.listen(5)

print("listening")

time.sleep(300)