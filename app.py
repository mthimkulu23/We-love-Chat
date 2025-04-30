from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, send
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/chatdb"
mongo = PyMongo(app)
socketio = SocketIO(app)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to render chat dashboard
@app.route('/chat')
def chat():
    return render_template('chat.html')

# Route to serve contacts as JSON
@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = mongo.db.contacts.find()
    contact_list = []
    for contact in contacts:
        contact_list.append({
            'id': str(contact['_id']),  # Mongo ObjectId to string
            'name': contact['name'],
            'lastMessage': contact.get('lastMessage', '')
        })
    return jsonify(contact_list)

# Route to serve past messages for a specific contact as JSON
@app.route('/messages', methods=['POST'])
def get_messages():
    data = request.json
    sender = data['sender']
    recipient = data['recipient']

    # Get messages where either sender or recipient matches
    messages = mongo.db.messages.find({
        "$or": [
            {'sender': sender, 'recipient': recipient},
            {'sender': recipient, 'recipient': sender}
        ]
    }).sort('timestamp', 1)

    return jsonify([
        {
            'username': msg['sender'],
            'message': msg['message'],
            'avatar': msg['avatar'],
            'timestamp': msg['timestamp']
        }
        for msg in messages
    ])

# WebSocket event to handle new message
@socketio.on('message')
def handle_message(data):
    data['timestamp'] = datetime.utcnow().isoformat()
    # Store the message in the messages collection and associate it with the sender and recipient
    mongo.db.messages.insert_one(data)
    send(data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
