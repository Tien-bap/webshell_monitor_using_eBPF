import socket

s = socket.socket()
s.connect(("192.168.2.7", 4444))
s.send(b"hello from container\n")
s.close()
