from flask import Flask, render_template, jsonify
from flask import request
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VoiceGrant
from twilio.twiml.voice_response import VoiceResponse, Dial
from dotenv import load_dotenv
import os
import pprint as p
from twilio.twiml.voice_response import VoiceResponse

load_dotenv()

account_sid = os.environ['TWILIO_ACCOUNT_SID']
api_key = os.environ['TWILIO_API_KEY_SID']
api_key_secret = os.environ['TWILIO_API_KEY_SECRET']
twiml_app_sid = os.environ['TWIML_APP_SID']
twilio_number = os.environ['TWILIO_NUMBER']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        'home.html',
        title="In browser calls",
    )

@app.route('/token', methods=['GET'])
def get_token():
    identity = twilio_number
    outgoing_application_sid = twiml_app_sid

    access_token = AccessToken(account_sid, api_key,
                               api_key_secret, identity=identity)

    voice_grant = VoiceGrant(
        outgoing_application_sid=outgoing_application_sid,
        incoming_allow=True


    )
    access_token.add_grant(voice_grant)

    response = jsonify(
        #{'token': access_token.to_jwt().decode(), 'identity': identity})
        {'token': access_token.to_jwt(), 'identity': identity})

    return response

@app.route('/handle_calls', methods=['POST'])

def call():
    p.pprint(request.form)
    response = VoiceResponse()

    #response.record(record='true')
    dial = Dial(callerId=twilio_number,record='true')


    if 'To' in request.form and request.form['To'] != twilio_number:
        print('outbound call')
        dial.number(request.form['To'])

    else:
        print('incoming call')
        caller = request.form['Caller']
        dial = Dial(callerId=caller)
        dial.client(twilio_number)



    return str(response.append(dial))


    return ''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)

'''
@app.route("/record", methods=['GET', 'POST'])

def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Hello. Please leave a message after the beep.')

    # Use <Record> to record the caller's message
    response.record(record=true)

    # End the call with <Hangup>
    response.hangup()

    return str(response)
'''