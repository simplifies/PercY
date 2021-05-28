import socket
import os
import sys

usercontact = "youruser2@percy.com"

default_server = "127.0.0.1"
default_server_port = 1884
contacts = {
    "youruser@percy.com" #add as many contacts as you want
}

user = os.getenv("USERNAME")

def client(ip, contact):

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socks.connect((ip, default_server_port))
    except:
        print("Couldn't connect")
        exit()
    firstrequest = socks.recv(1024).decode('ascii')
    if firstrequest == "USER":
        socks.send(usercontact.encode('ascii'))
    socks.send("send".encode('ascii'))
    message = input(">>> ")
    socks.send(message.encode('ascii'))
    socks.send(contact.encode('ascii'))

if sys.argv[1] in contacts:
  client(default_server, sys.argv[1])
else:
  print("Contact not found")
