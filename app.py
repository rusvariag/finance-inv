import os
from flask import Flask, request
from twilio.rest import Client

# Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
# twilio client
client = Client(account_sid, auth_token)

app = Flask(__name__)

# POST /call - send data to twilio
@app.route('/call', methods=['POST'])
def make_call():
    request_data = request.get_json()
    client.calls.create(
        method='GET',
        status_callback='https://www.myapp.com/events',
        status_callback_event=['ringing', 'answered', 'completed'],
        status_callback_method='POST',
        twiml='<Response><Say>Hello there, its me, your friend. Will you by this car from me?</Say></Response>',
        to=request_data['phoneNumber'],
        from_= os.environ['TWILIO_PHONE']
    )
    return call.sid

# POST /webhook - recieve data from twilio
@app.route('/webhook')
def twilio_webhooks():
    request_data = request.get_json()
    print(request_data)
    return 'Ok'

# GET / - serve html
@app.route('/', methods=['GET'])
def home():
    return 'Hello, world!'

app.run(host="10.0.0.100", port=3001)
