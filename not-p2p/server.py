import socket
import threading

# handle client
def handler(client_soc):
    client_soc.send("USER".encode('ascii'))
    user = client_soc.recv(1024).decode('ascii')
    firstresponse = client_soc.recv(1024).decode('ascii')
    if firstresponse == "send":
        secondresponse = client_soc.recv(1024).decode('ascii')
        contact = client_soc.recv(1024).decode('ascii')
        with open(contact + ".txt", "a") as f:
            f.write(user + ": " + secondresponse + "\n") # write message to contact file not the best way but for now it's ok
        client_soc.close()
    if firstresponse == "recieve":
        with open(user + ".txt", "r") as f:
            messages = f.read() # read messages
        client_soc.send(messages.encode('ascii'))
        client_soc.close()
        with open(user + ".txt", "w") as f2:
            f2.write("")

with socket.socket() as socks:
    socks.bind(('0.0.0.0', 1884))
    socks.listen()
    while True:
        client_soc, client_address = socks.accept()
        # create thread to handle client
        threading.Thread(target=handler,args=(client_soc,), daemon=True).start() 
