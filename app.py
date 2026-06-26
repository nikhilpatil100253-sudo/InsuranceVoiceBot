from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

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

    conversation_memory[call_sid] = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/process",
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
        action="/process",
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


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )