from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
# socketio = SocketIO(app)
app.config.from_object("config")  # Reads config.py contents and stores them into app.config

from LJ import views
