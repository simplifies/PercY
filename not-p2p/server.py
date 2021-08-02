from flask import Flask, render_template, request, abort, jsonify
import os, json

app = Flask(__name__)

@app.route("/api/create_user", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.headers
        username = data["user"]
        fernet_key = data["key"]
        if os.path.isdir("users/" + username):
            return "409", 409
        os.mkdir("users/" + username)
        os.mkdir("users/" + username + "/messages")
        with open("users/" + username + "/key.txt", "w") as f:
            f.write(fernet_key)
        return "200", 200

@app.route("/api/send_message", methods=["POST"])
def send_message():
    if request.method == "POST":
        data = request.headers
        message = data["message"]
        message_from = data["message_from"]
        fernet_key = data["key"]
        message_to = data["message_to"]
        with open("users/" + message_from + "/key.txt") as f:
            key = f.read()
        if fernet_key == key:
            if not os.path.isdir("users/" + message_to):
                abort(404)
            else:
                with open("users/" + message_from + "/messages/" + message_to + ".txt", "w") as f:
                    f.write(message_from + ": " + message)
                with open("users/" + message_to + "/messages/" + message_from + ".txt", "w") as f:
                    f.write(message_from + ": " + message)
                return "200", 200
        else:
            abort(401)

@app.route("/api/get_conversations", methods=["GET"])
def get_conversations():
    if request.method == "GET":
        data = request.headers
        username = data["user"]
        fernet_key = data["key"]
        with open("users/" + username + "/key.txt") as f:
            key = f.read()
        if fernet_key == key:
            files = os.listdir("users/" + username + "/messages")
            return jsonify(files)
        else:
            abort(401)

@app.route("/api/get_messages", methods=["GET"])
def get_messages():
    if request.method == "GET":
        data = request.headers
        username = data["user"]
        fernet_key = data["key"]
        conversation = data["conversation"]
        with open("users/" + username + "/key.txt") as f:
            key = f.read()
        if fernet_key == key:
            if not os.path.isfile("users/" + username + "/messages/" + conversation):
                abort(404)
            else:
                with open("users/" + username + "/messages/" + conversation, "r") as f:
                    messages = f.read()
                    messages = messages.split("\n")
                    return jsonify(messages)
        else:
            abort(401)

app.run()
