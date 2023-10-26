from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from http.server import BaseHTTPRequestHandler
from database import db
from flask_restful import Api, Resource
from flask_cors import CORS
from models import User, Message
from svix import Webhook
import os
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key = "hello"
SESSION_TYPE = "sqlalchemy"
# DB_URL = os.environ.get('DB_URL')
# DB_URL="postgresql://default:0kfNebo1Twgp@ep-hidden-rain-16108082.us-east-1.postgres.vercel-storage.com:5432/verceldb"
DB_URL = "postgresql://mbron770:14EXbZiTMBtz@ep-black-cherry-71826577.us-east-2.aws.neon.tech/neondb"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# @app.route('/display_all_users',  methods = ['GET', 'PATCH'])
# def test():
#     if(request.method == 'GET'):
#         all = User.query.all()
#         users = {}
#         for user in all:
#             users.append(str(user))
#         return jsonify(users), 200


@app.route('/display_all_users')
def display_all_users():
    # if(request.method == 'GET'):
    all = User.query.all()
    users = [user.to_dict() for user in all]
    # for user in all:
    #     # users[user.id] = str(user)
    #     # users[user.name] = str(user)
    #     # users[user.username] = str(user)
    #     users[user.id] = str(user)
    # return jsonify(users rules = ('-user.messages_received', '-messages_sent')), 200
    return jsonify({'users': users}), 200, {'X-Excluded-Fields': 'user.messages_received, messages_sent'}


# @app.route('/add_message_to_db', methods=['POST'])
# def add_message_to_db(): 
#     data = request.json()
#     request.get_json()
#     message = Message()
#     print(data)
#     try: 
#         for attr in data: 
#             setattr(message, attr, data[attr])
#         db.session.add(message)
#         db.session.commit()
#         return jsonify(message.to_dict())
#     except ValueError as ie: 
#         return {'error': ie.args}, 422

@app.route('/add_message_to_db', methods=['POST'])
def add_message_to_db(): 
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    try: 
        message = Message(**data)
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201
    except Exception as e:
        app.logger.error(f'Error adding message to database: {str(e)}')
        return jsonify({'error': 'Internal Server Error'}), 500
    


@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    # data = request.get_json()
    user = User()
    try:
        for attr in data:
            setattr(user, attr, data[attr])
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except ValueError as ie:
        return {'error': ie.args}, 422


@app.route('/update_user/<string:clerkID>', methods=['PATCH'])
def update_user(clerkID):
    user = User.query.filter_by(clerkID=clerkID).first()

    if not user:
        return {'error': 'user not found'}, 404
    data = request.json
    try:
        for attr in data:
            setattr(user, attr, data[attr])
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except ValueError as ie:
        return {'error': ie.args}, 422


@app.route('/delete_user/<string:deletedUserClerkID>', methods=['DELETE'])
def delete_user(deletedUserClerkID):
    user = User.query.filter_by(clerkID=deletedUserClerkID).first()
    if not user:
        return {'error': 'user not found'}, 404
    try:
        db.session.delete(user)
        db.session.commit()
        return {}, 201
    except ValueError as ie:
        return {'error': ie.args}, 422
    



@socketio.on('send_message')
def send_message(message):
    send(message)
    print(message)
    # message = {
    #     'user': data['user'],
    #     'text': data['text'],
    # }
    # messages.append(message)
    emit('got message', message, broadcast=True)


if __name__ == '__main__':
    # app.run(port=6000)
    socketio.run(app, port=10000, debug=True)
