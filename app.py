from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from db_service import create_call, update_call, update_status
from openai_service import get_ai_response, SYSTEM_PROMPT
from transcript import save_transcript

app = Flask(__name__)

# Store conversations per call
conversation_memory = {}


@app.route("/")
def home():
    return "Insurance AI Voice Bot Running Successfully"


@app.route("/voice", methods=["POST"])
def voice():

    call_sid = request.form.get("CallSid")
    create_call(
        call_sid=call_sid,
        customer_name="Nikhil Patil",
        phone_number="+919867005139",
        policy_number="Tata123"
    )
    conversation_memory[call_sid] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="https://insurancevoicebot-1.onrender.com/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )

    gather.say(
        """
        Hello Nikhil.

        Welcome to Tata Insurance.

        I am your AI Assistant.

        Can you please confirm your policy number?
        """,
        language="en-IN"
    )

    response.append(gather)

    return str(response)



@app.route("/process", methods=["POST"])
def process():

    call_sid = request.form.get("CallSid")

    speech = request.form.get("SpeechResult", "")

    print("Customer :", speech)

    save_transcript("Customer", speech)

    history = conversation_memory.get(call_sid)

    history.append(
        {
            "role": "user",
            "content": speech
        }
    )

    ai_response = get_ai_response(history)
    full_transcript = ""

    for msg in history:
        if msg["role"] != "system":
            full_transcript += f'{msg["role"]}: {msg["content"]}\n'

    update_call(
        call_sid=call_sid,
        status="Completed",
        transcript=full_transcript,
        summary="AI conversation completed successfully."
    )
    print("Bot :", ai_response)

    save_transcript("Bot", ai_response)

    history.append(
        {
            "role": "assistant",
            "content": ai_response
        }
    )

    conversation_memory[call_sid] = history

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="https://insurancevoicebot-1.onrender.com/process",
        method="POST",
        speech_timeout="auto",
        language="en-IN"
    )

    gather.say(

        ai_response,
        language="en-IN"
    )

    response.append(gather)

    return str(response)

@app.route("/status", methods=["POST"])
def status():

    call_sid = request.form.get("CallSid")
    call_status = request.form.get("CallStatus")

    print("Call SID:", call_sid)
    print("Call Status:", call_status)

    # Update database
    update_status(call_sid, call_status)

    return "OK"

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )