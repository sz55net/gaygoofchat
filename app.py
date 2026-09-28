from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = "furries rule the world."
socketio = SocketIO(app)



@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")

# @socketio.on("connect")
# def on_connect(auth):
#     print(auth)

@socketio.on("content_update")
def on_content_update(data):
    emit("content_update", {"data": data, "originator": request.sid}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
