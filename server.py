import socket
import termcolor


def target_communication():
    message = target.recv(1024)
    print(message.decode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 777))
print(termcolor.colored("(#) LISTENING FOR INCOMING CONNECTIONS (#)", 'yellow'))
sock.listen(5)


target, ip = sock.accept()
print(termcolor.colored(f"(!) TARGET CONNECTED FROM {ip} (!)", 'green'))
target_communication()
