import os
from flask import Flask, render_template, url_for, redirect, request
from flask_socketio import SocketIO, join_room, leave_room, send
from pymongo.errors import DuplicateKeyError

from forms import UserForm, ChatBox
from counter import Counter
from db import save_user, save_room, add_member, remove_room_member, is_room_member, is_room_admin, room_exists, remove_user

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'this-is-a-secret-key-for-this'
socketio = SocketIO(app)

counter = Counter()

@app.route("/", methods=["GET", "POST"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        try:
            save_user(form.name.data)
        except DuplicateKeyError:
            print("name error")
            return render_template("index.html", form=form, message="User already exists")

        if form.create.data:
            try:
                save_room(form.room.data, form.name.data)
            except DuplicateKeyError:
                print("room exists")
                remove_user(form.name.data)
                return render_template("index.html", form=form, message="Cannot create room which already exists")

        if form.join.data:
            if not room_exists(form.room.data):
                print("room doesn't exists")
                remove_user(form.name.data)
                return render_template("index.html", form=form, message="Cannot join room which doesn't exists")

            add_member(form.room.data, form.name.data)

        return redirect(url_for("lobby", user=form.name.data, room=form.room.data))
    return render_template("index.html", form=form, message = '')

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
    json['id'] = "msg" + str(counter.next())
    socketio.emit('my response', json, room=json['room'], callback=messageReceived)

@app.route("/lobby/", defaults={'room' : 'main', 'user' : 'Anon'}, methods=["GET", "POST"])
@app.route("/lobby/<room>/<user>", methods=["GET", "POST"])
def lobby(room, user):
    if request.referrer != None and request.referrer in request.base_url:
        form = ChatBox()
        if form.validate_on_submit():
            return redirect(url_for("lobby", user=user, room=room))

        return render_template("lobby.html", form=form, user=user, room=room)
    else:
        return redirect(url_for("index"))

if __name__ == 'main':
    socketio.run(app, debug=True)