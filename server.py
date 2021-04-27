import socket, sys, playsound

with open("messages.txt", "w") as messages:
    messages.write("")

host = '0.0.0.0'
port = 1481

sockserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockserver.bind((host, port))
sockserver.listen()

def sound():
    playsound.playsound("trillo.mp3")

def server():
    while True:
        client, address = sockserver.accept()
        client.send("USER".encode('ascii'))
        hostname = client.recv(1024).decode('ascii')
        hostname = str(hostname) + "@" + str(address[0])
        message = hostname + "> " + client.recv(1024).decode('ascii') 
        print(message)  
        sound()
        with open("messages.txt", "a") as messages:
            messages.write(message + "\n")

server()