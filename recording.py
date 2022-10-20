

































'''
import requests
from flask import Flask, request
from twilio.twiml.voice_response import Record, VoiceResponse

app = Flask(__name__)

@app.route("/recording-complete", methods=['GET', 'POST'])
def recording_complete():
    response = VoiceResponse()

    # The recording url will return a wav file by default, or an mp3 if you add .mp3
    recording_url = request.values['RecordingUrl'] + '.mp3'

    filename = request.values['RecordingSid'] + '.mp3'
    with open('{}/{}'.format("directory/to/download/to", filename), 'wb') as f:
        f.write(requests.get(recording_url).content)

    return str(response)


@app.route("/record", methods=['GET', 'POST'])
def record():
    """Returns TwiML which prompts the caller to record a message"""
    # Start our TwiML response
    response = VoiceResponse()

    # Use <Say> to give the caller some instructions
    response.say('Hello. Please leave a message after the beep.')

    # Use <Record> to record the caller's message
    response.record()

    # End the call with <Hangup>
    response.hangup()

    return str(response)
'''
if __name__ == "__main__":
    app.run()
