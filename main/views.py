import datetime
import json
import random

import requests
from django.conf import settings
from django.shortcuts import render
from django.db.models.functions import (ExtractDay, ExtractHour, ExtractMinute,
                                        ExtractMonth, ExtractQuarter, ExtractSecond,
                                        ExtractWeek, ExtractIsoWeekDay, ExtractWeekDay,
                                        ExtractIsoYear, ExtractYear)
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from . import tasks
from main.models import UserInfo
from main.serializers import TaskScheduleSerializer

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = settings.BOT_TOKEN


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def start(request):
    data = request.data
    print(data)
    if data['message']['text'] == "/start":
        userChatID = data['message']['from']['id']
        created_id = random.randint(111111111111, 999999999999)
        info, created = UserInfo.objects.get_or_create(userID=userChatID)
        if created:
            info.taskID = created_id
            data = {
                "chat_id": userChatID,
                "text": f"Thank you for reaching out, the id for linking your account is {created_id}",
                "parse_mode": "Markdown",
            }
            response = requests.post(
                f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
            )
            info.save()
            return Response({}, status=200)
        else:
            data = {
                "chat_id": userChatID,
                "text": "You have already linked this account",
                "parse_mode": "Markdown",
            }
            response = requests.post(
                f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
            )
            return Response({}, status=200)
    else:
        userChatID = data['message']['from']['id']
        data = {
            "chat_id": userChatID,
            "text": f"Invalid command.\nUse the /start command to start a convo with this bot.",
            "parse_mode": "Markdown",
        }
        response = requests.post(
            f"{TELEGRAM_URL}{TUTORIAL_BOT_TOKEN}/sendMessage", data=data
        )
        return Response({}, status=200)


@swagger_auto_schema(method='post', request_body=TaskScheduleSerializer)
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def schedule(request):
    data = request.data
    serialized = TaskScheduleSerializer(data=data)
    if serialized.is_valid(raise_exception=True):
        time = serialized.data.get("time")
        y, mo, d, h, m = parseTime(time)
        description = serialized.data.get("description")
        id = serialized.data.get("userID")
        print(id)
        info = get_object_or_404(UserInfo, taskID=id)
        print(info)
        id = info.userID
        name = str(description) + " " + str(id)
        schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h, minute=m)
        task = PeriodicTask.objects.create(crontab=schedule, name=name, task="sendReminder",
                                           args=json.dumps([id, description]))
        return Response({}, status=200)


def parseTime(date_time):
    print(date_time)
    date, time = date_time.split("T")
    year, month, day = date.split("-")
    hour, minute, k, v = time.split(":")
    return int(year), int(month), int(day), int(hour), int(minute)
