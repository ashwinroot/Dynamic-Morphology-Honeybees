from LJ import app
from flask_socketio import SocketIO

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # socketio = SocketIO(app)
    # socketio.run(app, port=5000, debug=True, use_reloader=True)
