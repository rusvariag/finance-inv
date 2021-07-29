import os
from flask import Flask, Response, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import Dial, VoiceResponse

# app  
app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

# GET / - server static files
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route("/token", methods=["GET"])
def token():
    # get credentials for environment variables
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    application_sid = os.environ["TWILIO_TWIML_APP_SID"]
    api_key = os.environ["API_KEY"]
    api_secret = os.environ["API_SECRET"]

    # Create access token with credentials
    token = AccessToken(account_sid, api_key, api_secret)

    # Create a Voice grant and add to token
    voice_grant = VoiceGrant(
        outgoing_application_sid=application_sid,
    )
    token.add_grant(voice_grant)

    # Return token info as JSON
    token = token.to_jwt()

    # Return token info as JSON
    return jsonify(token=token.decode("utf-8"))


@app.route("/voice", methods=["POST"])
def voice():
    resp = VoiceResponse()

    # Placing an outbound call from the Twilio client
    dial = Dial(caller_id=os.environ['TWILIO_PHONE'], timeout=10)

    # specify number and webhooks
    dial.number(request.form["phone"], 
        status_callback_event='initiated ringing answered completed',
        status_callback=os.environ['WEBHOOK'],
        status_callback_method='POST'
    )

    resp.append(dial)

    return Response(str(resp), mimetype="text/xml")


# POST /webhook - recieve data from twilio
@app.route('/webhook', methods=['POST'])
def twilio_webhooks():
    socketio.emit('newStatus', request.form.get('CallStatus'))
    return 'Ok'

app.run(port=os.environ['PORT'])
