from flask import Flask, request, jsonify
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
 
app = Flask(__name__)
 
# Set your Twilio credentials
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
 
# If you want to store the phone number in an environment variable, you can do that too.
# Or you can fetch it from a database or pass it through the request in the /make_call endpoint.
 
@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    # Ask for the user's name
    response.say("Hi, I am your bot. What is your name?")
    response.record(timeout=10, transcribe=True, max_length=30, action='/record_name')
    return str(response)
 
@app.route("/record_name", methods=['POST'])
def record_name():
    user_name = request.form.get('TranscriptionText')
    response = VoiceResponse()
    # Ask for the user's age
    response.say(f"Nice to meet you, {user_name}. What is your age?")
    response.record(timeout=10, transcribe=True, max_length=30, action='/record_age')
    return str(response)
 
@app.route("/record_age", methods=['POST'])
def record_age():
    user_age = request.form.get('TranscriptionText')
    response = VoiceResponse()
    # Ask for the user's gender
    response.say(f"Got it, you are {user_age} years old. What is your gender?")
    response.record(timeout=10, transcribe=True, max_length=30, action='/record_gender')
    return str(response)
 
@app.route("/record_gender", methods=['POST'])
def record_gender():
    user_gender = request.form.get('TranscriptionText')
    response = VoiceResponse()
    # Thank the user and conclude the call
    response.say(f"Thank you for sharing, you are {user_gender}. Have a great day!")
    return str(response)
 
# Make a call to a number
@app.route("/make_call", methods=['POST'])
def make_call():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    # Fetch the phone number from request data or hardcode a number (for demo purposes)
    to_number = request.json.get('to')  # You can also hardcode this value or fetch from a database
    if not to_number:
        return jsonify({"error": "Recipient phone number is required"}), 400
    try:
        # Create a call to the specified number
        call = client.calls.create(
            to=to_number,  # The number you are calling
            from_=TWILIO_PHONE_NUMBER,  # Your Twilio number
            url="https://your-render-app-url/voice"  # The URL that handles the voice interaction
        )
        return jsonify({"sid": call.sid, "message": "Call initiated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)