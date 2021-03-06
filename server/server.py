from flask import Flask, render_template, request, abort, jsonify
import os, json

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.route("/api/create_user", methods=["POST"])
def create_user():
    if request.method == "POST":
        data = request.headers
        username = data["user"]
        fernet_key = data["key"]
        if os.path.isdir("users/" + username):
            return "409", 409
        if "." or "/" in username:
            return "400", 400
        os.mkdir("users/" + username)
        os.mkdir("users/" + username + "/messages")
        with open("users/" + username + "/" + username + fernet_key, "w") as f:
            f.write(fernet_key)
        return "200", 200

@app.route("/api/login", methods=["GET"])
def login():
    if request.method == "GET":
        data = request.headers
        key = data["key"]
        user = data["user"]
        if os.path.isdir("users/" + user):
            if os.path.isfile("users/" + user + "/" + user + key):
                return "200", 200
            else:
                abort(401)
        else:
            abort(404)
    
@app.route("/api/send_message", methods=["POST"])
def send_message():
    if request.method == "POST":
        data = request.headers
        message = data["message"]
        message_from = data["message_from"]
        fernet_key = data["key"]
        message_to = data["message_to"]
        if os.path.isfile("users/" + message_from + "/" + message_from + fernet_key):
            if not os.path.isdir("users/" + message_to):
                abort(404)
            else:
                with open("users/" + message_from + "/messages/" + message_to, "a") as f:
                    f.write(message_from + ": " + message)
                with open("users/" + message_to + "/messages/" + message_from, "a") as f:
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
        if os.path.isfile("users/" + username + "/" + username + fernet_key):
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
        if os.path.isfile("users/" + username + "/" + username + fernet_key):
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
