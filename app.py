import os
from flask import Flask
from twilio.rest import Client

# Account SID from twilio.com/console
account_sid = os.environ['TWILIO_ACCOUNT_SID']
# Auth Token from twilio.com/console
auth_token  = os.environ['TWILIO_AUTH_TOKEN']
# twilio client
client = Client(account_sid, auth_token)

app = Flask(__name__)
# route decorator for call
@app.route('/call')
def home():
    client.calls.create(
                        twiml='<Response><Say>Ahoy, World!</Say></Response>',
                        to='+9711111',
                        from_= os.environ['TWILIO_PHONE']
                    )
    return 'Hello, world!'

app.run(host="10.0.0.100", port=3001)