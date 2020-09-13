import os
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGO_KEY'))

chat = client.get_database("Chat")
users = chat.get_collection("users")
rooms = chat.get_collection("rooms")
room_members = chat.get_collection("room_members")

def save_user(user):
    users.insert_one({'_id' : user})

def save_room(room, admin):
    rooms.insert_one({'_id' : room, 'admin' : admin})
    add_member(room, admin, True)

def add_member(room, user, isAdmin=False):
    room_members.insert_one({'_id' : {'room' : room, 'user' : user}, 'isAdmin' : isAdmin})

def remove_room_member(room, user):
    if (is_room_admin(room, user)):
        rooms.delete({'_id' : room})
    room_members.delete_one({'_id' : {'room' : room, 'user' : user}})

def remove_user(user):
    users.delete_one({'_id' : user})

def room_exists(room):
    return rooms.count_documents({'_id' : room}) > 0

def is_room_member(room, user):
    return room_members.count_documents({'_id' : {'room' : room, 'user' : user}}) > 0

def is_room_admin(room, user):
    return room_members.count_documents({'_id' : {'room' : room, 'user' : user}, 'isAdmin' : True}) > 0