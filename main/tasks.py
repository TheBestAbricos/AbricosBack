import requests
from celery import shared_task
from django.conf import settings

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = settings.BOT_TOKEN


@shared_task
def sendReminder(userID, message):
    data = {
        "chat_id": userID,
        "text": f"This is reminder that you have a task described as {message}.\nYou are getting this because you "
                f"connected your device with the task app",
        "parse_mode": "Markdown",
    }
    response = requests.post(
        f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
    )
