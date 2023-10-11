from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from http.server import BaseHTTPRequestHandler
from database import db
from flask_restful import Api, Resource
from flask_cors import CORS
from models import User
from svix import Webhook
import os

app = Flask(__name__)
CORS(app)
api = Api(app)
app.secret_key="hello"
SESSION_TYPE="sqlalchemy"
# DB_URL = os.environ.get('DB_URL')
# DB_URL="postgresql://default:0kfNebo1Twgp@ep-hidden-rain-16108082.us-east-1.postgres.vercel-storage.com:5432/verceldb"
DB_URL="postgresql://mbron770:14EXbZiTMBtz@ep-black-cherry-71826577.us-east-2.aws.neon.tech/neondb"
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test',  methods = ['GET', 'PATCH'])
def test():
    if(request.method == 'GET'):
        all = User.query.all()
        users = []
        for user in all:
            users.append(str(user))
        return jsonify(users), 200
    
@app.route('/clerk_webhook', methods = ['POST'])
def webhook_handler():
    if request.method != 'POST': return ('Method Not Allowed', 405)
    # return jsonify('hhwewqwwqwq'),200
    
    # payload = request.json
    # headers = request.headers
    clerk_secret = 'whsec_l47H70e5eo5F3Uvv4vlVRgMaYITINbdK'
    
    # heads = {
    #     'svix-id': headers.get('svid-id'), 
    #     'svix-timestamp': headers.get('svix-timestamp'), 
    #     'svix-signature': headers.get('svix-signature'),
    # }
    
    # wh = Webhook(clerk_secret)
    
    try:
        payload = request.get_json()
        svix_id = request.headers.get('svid-id')
        svix_timestamp = request.headers.get('svix-timestamp')
        svix_signature = request.headers.get('svix-signature')
        wh = Webhook(clerk_secret)
        evt = wh.verify(request.data, svix_id, svix_timestamp, svix_signature)
        
        if(evt.type in ['user.created', 'user.updated', ]): 
        #    print('User created/updated', evt.data)
           print('User created/updated', evt.data)
           
            # data = request.json()
            # user = User()
            # try:
            #     for attr in data: 
            #         setattr(user, attr, data[attr])
            #     db.session.add(user)
            #     db.session.commit()
            #     print('User created/updated', evt.data)
            # except ValueError as ie: 
            #     return {'error': ie.args}, 422
            
            
        elif(evt.type == 'user.deleted'): print('user deleted:', evt.data)
        return jsonify({'success': True}), 200
    except Exception as e: 
        return jsonify({'error': 'failed'}), 400
        
    
    
    
    
    


    # if __name__ == '__main__':
    #     app.run(port=6000)

