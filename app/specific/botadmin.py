from flask import Blueprint
from flask_restful.representations import json
from flask_socketio import emit


botadmin = Blueprint('botadmin', __name__)
#
#
# @socket.on('message')
# def handle_message(message):
#     print(message)
#     socket.emit("roufa_minima","Ante kai gamisou")
#
#
# def update(data):
#     data = json.dumps(data)
#     socket.emit('roufa_minima', data, broadcast=True)
