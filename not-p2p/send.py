from cryptography.fernet import Fernet
import requests, json, os

def generate_key():
    key = Fernet.generate_key()
    with open("storage/key.key", "wb") as f:
        f.write(key)
    return key

def create_user(user, key):
    data = {
        "user": user, 
        "key": key
    }
    rq = requests.post("http://127.0.0.1:5000/api/create_user", headers=data)
    if rq.status_code == 200:
        print("Account successfully created!")
    if rq.status_code == 409:
        print("Account already exists")
        exit()

def get_conversations(user,key):
    data = {
        "user": user, 
        "key": key
    }
    rq = requests.get("http://127.0.0.1:5000/api/get_conversations", headers=data)
    convs = json.loads(rq.text)
    print("---- CONVERSATIONS ----")
    for i in convs:
        print(i)
    print("\m")

def get_messages(user,key,conversation):
    data = {
        "user": user, 
        "key": key,
        "conversation": conversation
    }
    rq = requests.get("http://127.0.0.1:5000/api/get_messages", headers=data)
    data = json.loads(rq.text)
    print("---- MESSAGES ----")
    for i in data:
        print(i)
    print("\n")

def send_messages(to,fromm,key,message):
    data = {
        "message_to": to,
        "message_from": fromm,
        "key": key,
        "message": message
    }
    rq = requests.post("http://127.0.0.1:5000/api/send_message", headers=data)
    if rq.status_code == 200:
        print("Message sent!")

def main():
    help_list = """list: List all conversations
    send_message: send a message to someone
    get_messages: get messages
    exit: exit percy
    """
    if not os.path.isfile("storage/user.txt"):
        print(os.path.isfile("storage/user.txt"))
        key = generate_key()
        print("Enter username")
        user = input(">>> ")
        with open("storage/user.txt", "w") as f:
            f.write(user)
        create_user(user, key)
        print(help_list)
        while True:
            inp = input(">>> ")
            if inp == "list":
                get_conversations(user, key)
            if inp.startswith("send_message"):
                to = input("Enter target user: ")
                message = input("Enter message: ")
                send_messages(to,user,key,message)
            if inp.startswith("get_messages"):
                conv = input("Enter conversation: ")
                get_messages(user,key,conv)
            if inp.startswith("exit"):
                print("Exiting...")
                exit()
    else:
        print(help_list)
        with open("storage/key.key", "r") as f:
            key = f.read()
        with open("storage/user.txt", "r") as f:
            user = f.read()
        while True:
            inp = input(">>> ")
            if inp == "list":
                get_conversations(user, key)
            if inp.startswith("send_message"):
                to = input("Enter target user: ")
                message = input("Enter message: ")
                send_messages(to,user,key,message)
            if inp.startswith("get_messages"):
                conv = input("Enter conversation: ")
                get_messages(user,key,conv)
            if inp.startswith("exit"):
                print("Exiting...")
                exit()

main()
