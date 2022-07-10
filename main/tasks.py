import requests
from celery import shared_task
from django.conf import settings

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = settings.BOT_TOKEN


@shared_task
def sendReminder(userID, message):
    data = {
        "chat_id": userID,
        "text": f"Hello from Abricos🤖\nYou have a task described as:\n{message}",
        "parse_mode": "Markdown",
    }
    response = requests.post(
        f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
    )
