from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Routes

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([message.serialize() for message in messages])

@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404
    return jsonify(message.serialize())

@app.route('/messages', methods=['POST'])
def create_message():
    body = request.json.get('body')
    username = request.json.get('username')

    if not body or not username:
        return jsonify({'error': 'Missing body or username'}), 400

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()

    return jsonify(message.serialize()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    body = request.json.get('body')

    if body:
        message.body = body
        message.updated_at = datetime.utcnow()
        db.session.commit()

    return jsonify(message.serialize())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return jsonify({'error': 'Message not found'}), 404

    db.session.delete(message)
    db.session.commit()

    return jsonify({'message': 'Message deleted successfully'})

if __name__ == '__main__':
    app.run(port=5555)
