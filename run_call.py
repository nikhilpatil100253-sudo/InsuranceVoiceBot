from twilio.rest import Client
from config import (
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    TWILIO_PHONE_NUMBER,
)

# ----------------------------
# Customer Details
# ----------------------------
CUSTOMER_NUMBER = "+919867005139"

# ----------------------------
# IMPORTANT
# Replace with your Render URL after deployment
# Example:
# https://insurancevoicebot.onrender.com/voice
# ----------------------------
VOICE_URL = "https://YOUR_RENDER_URL.onrender.com/voice"

client = Client(
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN
)

call = client.calls.create(
    to=CUSTOMER_NUMBER,
    from_=TWILIO_PHONE_NUMBER,
    url=VOICE_URL,
    method="POST"
)

print("=" * 50)
print("Call Initiated Successfully")
print("Call SID :", call.sid)
print("=" * 50)