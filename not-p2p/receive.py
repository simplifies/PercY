import socket
import os
import sys

usercontact = "youruser@percy.com" #change to your user 
 
default_server = "127.0.0.1" #change to your server ip
default_server_port = 1884
user = os.getenv("USERNAME")

def client():

    socks = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socks.connect((default_server, default_server_port))
        firstrequest = socks.recv(1024).decode('ascii')
        if firstrequest == "USER":
            socks.send(usercontact.encode('ascii'))
            pass
        socks.send("recieve".encode('ascii'))
        message = socks.recv(1024).decode('ascii')
        print("Your inbox: ")
        print(message)
        print("Finished inbox")
    except:
        print("Couldn't connect")
        exit()
    

client()
