import os

from flask import Flask, render_template, request, redirect, send_from_directory
from flask_socketio import SocketIO, emit, join_room
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["SECRET_KEY"] = "furries rule the world."
socketio = SocketIO(app)

last_update  = ""

# add gifs in text.
@app.route('/')
def hello_world():
    filelist = os.listdir("./user_uploads")
    return render_template("index.html", filelist=filelist)

@socketio.on("connect")
def on_connect(auth):
    global last_update
    emit("content_update", {"data": last_update, "originator": "initial-connection"})

@socketio.on("content_update")
def on_content_update(data):
    global last_update
    last_update = data
    emit("content_update", {"data": data, "originator": request.sid}, broadcast=True)

@app.route("/gifUpload", methods=["POST"])
def upload_gif():
    print(request.files["file"])
    request.files["file"].save("./user_uploads/"+secure_filename(request.files["file"].filename))
    return redirect("/", 303)

@app.route("/udl/<filename>")
def udl(filename):
    return send_from_directory("./user_uploads", filename)


if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True, host="0.0.0.0")
