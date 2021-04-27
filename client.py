import socket
import os
import sys

contacts = {
    "Echo": "127.0.0.1"
}

user = os.getenv("USERNAME")

def client(ip):
    port = 1481

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socks.connect((ip, port))
    except:
        print("Couldn't connect")
        exit()
    
    firstrequest = socks.recv(1024).decode('ascii')
    if firstrequest == "USER":
        socks.send(user.encode('ascii'))
    message = input(">>> ")
    socks.send(message.encode('ascii'))

try:
    if contacts.get(sys.argv[1]):
        contact = contacts.get(sys.argv[1])
        client(contact)
    else:
        client(sys.argv[1])
except:
    print("Please provide an IP or contact")
