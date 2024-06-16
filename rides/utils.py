# utils.py

from django.conf import settings
from twilio.rest import Client

def send_sms(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=to
    )
    print(message.sid)
    return message.sid

def send_whatsapp(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=body,
        from_='whatsapp:' + settings.TWILIO_PHONE_NUMBER,
        to='whatsapp:' + to
    )
    return message.sid
