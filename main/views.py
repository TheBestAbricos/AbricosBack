from .views_import import *

TELEGRAM_URL = "https://api.telegram.org/bot"
TUTORIAL_BOT_TOKEN = settings.BOT_TOKEN


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def start(request):
    data = request.data
    if data['message']['text'] == "/start":
        userChatID = data['message']['from']['id']
        created_id = random.randint(111111111111, 999999999999)
        info, created = UserInfo.objects.get_or_create(userID=userChatID)
        if created:
            info.taskID = created_id
            data = {
                "chat_id": userChatID,
                "text": f"Thank you for reaching out, the token for linking your account is {created_id}",
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
        name = serialized.data.get("name")
        token = serialized.data.get("token")
        info = get_object_or_404(UserInfo, taskID=token)
        userID = info.userID
        name_title = str(name) + " " + str(token)
        schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h, minute=m)
        task = PeriodicTask.objects.create(crontab=schedule, name=name_title, task="main.tasks.sendReminder",
                                           args=json.dumps([userID, name]), one_off=True)
        return Response({}, status=200)


@swagger_auto_schema(method='patch', request_body=EditTaskSerializer)
@api_view(['PATCH'])
@csrf_exempt
@permission_classes([AllowAny])
def editSchedule(request):
    serialized = EditTaskSerializer(data=request.data)
    if serialized.is_valid(raise_exception=True):
        old_name = serialized.data.get("old_name")
        token = serialized.data.get("token")
        name = str(old_name) + " " + str(token)
        if serialized.data.get("new_name") and serialized.data.get("new_time"):
            task = get_object_or_404(PeriodicTask, name=name)
            new_name = serialized.data.get("new_name")
            new_time = serialized.data.get("new_time")
            y, mo, d, h, m = parseTime(new_time)
            new_schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
                                                                          minute=m)
            task.crontab = new_schedule
            task.name = new_name
            task.save()
            return Response({}, status=200)
        elif serialized.data.get("new_name"):
            new_name = serialized.data.get("new_name")
            task = get_object_or_404(PeriodicTask, name=name)
            task.name = new_name
            task.save()
            return Response({}, status=200)
        elif serialized.data.get("new_time"):
            task = get_object_or_404(PeriodicTask, name=name)
            new_time = serialized.data.get("new_time")
            y, mo, d, h, m = parseTime(new_time)
            new_schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
                                                                          minute=m)
            task.crontab = new_schedule
            task.save()
            return Response({}, status=200)
        else:
            return Response({"message": "No field to change was provided"}, status=400)


@swagger_auto_schema(method='get')
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def unlinkTelegram(request, token):
    userInfo = get_object_or_404(UserInfo, taskID=token)
    userInfo.delete()
    return Response({}, status=200)


@swagger_auto_schema(method='delete', request_body=DeleteTaskScheduleSerializer)
@api_view(['delete'])
@csrf_exempt
@permission_classes([AllowAny])
def deleteSchedule(request):
    serialized = DeleteTaskScheduleSerializer(data=request.data)
    if serialized.is_valid(raise_exception=True):
        token = serialized.data.get("token")
        name = serialized.data.get("name")
        name = str(name) + " " + str(token)
        task = get_object_or_404(PeriodicTask, name=name)
        task.delete()
        return Response({}, status=200)
