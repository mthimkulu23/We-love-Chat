from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)

# Simple user data for demo purposes (replace with actual user authentication)
users = {"test@example.com": "password123"}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    
    if email in users and users[email] == password:
        return redirect(url_for('chat'))
    else:
        return "Invalid credentials", 401

@app.route('/chat')
def chat():
    return render_template('chat.html')

# SocketIO event to handle incoming messages
@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
