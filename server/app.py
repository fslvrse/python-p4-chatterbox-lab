from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_msg = Message(body=data.get('body'), username=data.get('username'))
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()),201

@app.route('/messages', methods=['GET'])
def get_messages():
    messages= Message.query.order_by(Message.created_at).all()
    return jsonify([msg.to_dict() for msg in messages]),200

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    msg = db.session.get(Message, id)
    if not msg:
        return jsonify({'error': 'Message not found'}), 404
    data = request.get_json()
    if 'body' in data:
        msg.body = data['body']
    if 'username' in data:
        msg.username = data['username']
    db.session.commit()
    return jsonify(msg.to_dict()), 200

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    msg=db.session.get(Message, id)
    if not msg:
        return jsonify({'error': 'Message not found'}),404
    db.session.delete(msg)
    db.session.commit()
    return jsonify({'message':'Delete'}),200
    

if __name__ == '__main__':
    app.run(port=5555)