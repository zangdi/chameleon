import os
from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO, join_room, leave_room, send

from forms import UserForm, ChatBox

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'this-is-a-secret-key-for-this'
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        return redirect(url_for("lobby", user=form.name.data, room=form.room.data))
    return render_template("index.html", form=form)

def messageReceived(methods=["GET", "POST"]):
    print('message was received')

@socketio.on('join')
def on_join(data):
    user = data['user']
    room = data['room']
    join_room(room)
    print(user + ' has joined ' + room)
    send(user + ' has joined ' + room, room=room)

@socketio.on('my event')
def handle_receive_message(json, methods=["GET", "POST"]):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, room=json['room'], callback=messageReceived)

@app.route("/lobby/", defaults={'room' : 'main', 'user' : 'Anon'}, methods=["GET", "POST"])
@app.route("/lobby/<room>/<user>", methods=["GET", "POST"])
def lobby(user, room):
    print(user)
    form = ChatBox()
    if form.validate_on_submit():
        return redirect(url_for("lobby", user=user, room=room))

    return render_template("lobby.html", form=form, user=user, room=room)

if __name__ == 'main':
    socketio.run(app, debug=True)