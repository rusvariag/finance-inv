import os
from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from twilio.rest import Client

# Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
# twilio client
client = Client(account_sid, auth_token)

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


# POST /call - send data to twilio
@app.route('/call', methods=['POST'])
def make_call():
    request_data = request.get_json()
    call = client.calls.create(
        method='GET',
        status_callback='https://1729e2371628.ngrok.io/webhook',
        status_callback_event=['initiated', 'ringing', 'answered', 'completed'],
        status_callback_method='POST',
        twiml='<Response><Say>Hello there, its me, Ivan. Will you by this car from me?</Say></Response>',
        to=request_data['phoneNumber'],
        from_= os.environ['TWILIO_PHONE']
    )
    return jsonify(call.sid)

# POST /webhook - recieve data from twilio
@app.route('/webhook', methods=['POST'])
def twilio_webhooks():
    socketio.emit('newStatus', request.form.get('CallStatus'))
    return 'Ok'

# GET / - serve html
@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'

app.run(port=os.environ['PORT'])
