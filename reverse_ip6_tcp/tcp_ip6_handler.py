#!/usr/bin/env python
import socket
import sys
import os
ip = "::"
port = 1472 
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM) 
s.bind((ip, port))
s.listen(1)
conn, addr = s.accept()
print addr, " has connected"
while True:
        try:
            x = raw_input('>>')
            conn.sendall(x+ '\n')
	    data = conn.recv(1024)
	    sys.stdout.write(data)
        except:
            s.close()
            print ''
            exit()

