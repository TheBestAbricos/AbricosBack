import pytz

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
            info.token = created_id
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
                "text": f"You have already linked this account\nYour token is {info.token}",
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


@swagger_auto_schema(method='get')
@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def ifTokenExist(request, token):
    userToken = get_object_or_404(UserInfo, taskID=token)
    if userToken:
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
        token = serialized.data.get("token")
        user = get_object_or_404(UserInfo, token=token)
        description = serialized.data.get("description")
        y, mo, d, h, m = parseTime(time)
        time = datetime.datetime(year=y, month=mo,
                                 day=d, hour=h, minute=m)
        taskID = serialized.data.get("taskID")
        toDo = Task.objects.filter(taskID=taskID)
        if toDo.exists():
            task = PeriodicTask.objects.filter(name=taskID).first()
            task.delete()
            toDo.delete()
            toDO = Task.objects.create(
                taskID=taskID,
                user=user,
                description=description,
                time=time
            )
            schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
                                                                      minute=m)
            task = PeriodicTask.objects.create(crontab=schedule, name=taskID, task="main.tasks.sendReminder",
                                               args=json.dumps([user.userID, description]), one_off=True)
            return Response({}, status=200)

        else:
            toDO = Task.objects.create(
                taskID=taskID,
                user=user,
                description=description,
                time=time
            )
            schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
                                                                      minute=m)
            task = PeriodicTask.objects.create(crontab=schedule, name=taskID, task="main.tasks.sendReminder",
                                               args=json.dumps([user.userID, description]), one_off=True)
            return Response({}, status=200)

        # name = serialized.data.get("descri")
        # token = serialized.data.get("token")
        # idt = serialized.data.get("id")
        # info = get_object_or_404(UserInfo, taskID=token)
        # userID = info.userID
        # name_title = str(name) + " " + str(token) + " " + idt
        # schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h, minute=m)
        # task = PeriodicTask.objects.create(crontab=schedule, name=name_title, task="main.tasks.sendReminder",
        #                                    args=json.dumps([userID, name]), one_off=True)
        # return Response({}, status=200)


# @swagger_auto_schema(method='patch', request_body=EditTaskSerializer)
# @api_view(['PATCH'])
# @csrf_exempt
# @permission_classes([AllowAny])
# def editSchedule(request):
#     pass
# serialized = EditTaskSerializer(data=request.data)
# if serialized.is_valid(raise_exception=True):
#     old_name = serialized.data.get("old_name")
#     token = serialized.data.get("token")
#     idt = serialized.data.get("id")
#     name = str(old_name) + " " + str(token) + " " + idt
#     userID = get_object_or_404(UserInfo, taskID = token).userID
#     if serialized.data.get("new_name") and serialized.data.get("new_time"):
#         task = get_object_or_404(PeriodicTask, name=name)
#         new_name = serialized.data.get("new_name")
#         new_name_2 = serialized.data.get("new_name") + " " + str(token) + " " + idt
#         new_time = serialized.data.get("new_time")
#         y, mo, d, h, m = parseTime(new_time)
#         new_schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
#                                                                       minute=m)
#         task.crontab = new_schedule
#         task.name = new_name_2
#         task.args = json.dumps([userID, new_name])
#         task.save()
#         return Response({}, status=200)
#     elif serialized.data.get("new_name"):
#         new_name = serialized.data.get("new_name")
#         new_name_2 = serialized.data.get("new_name") + " " + str(token) + " " + idt
#         task = get_object_or_404(PeriodicTask, name=name)
#         task.name = new_name_2
#         task.args = json.dumps([userID, new_name])
#         task.save()
#         return Response({}, status=200)
#     elif serialized.data.get("new_time"):
#         task = get_object_or_404(PeriodicTask, name=name)
#         new_time = serialized.data.get("new_time")
#         y, mo, d, h, m = parseTime(new_time)
#         new_schedule, created = CrontabSchedule.objects.get_or_create(month_of_year=mo, day_of_month=d, hour=h,
#                                                                       minute=m)
#         task.crontab = new_schedule
#         task.save()
#         return Response({}, status=200)
#     else:
#         return Response({"message": "No field to change was provided"}, status=400)


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
    data = request.data
    serialized = DeleteTaskScheduleSerializer(data=data)
    if serialized.is_valid(raise_exception=True):
        toDo = get_object_or_404(Task, taskID=serialized.data.get("taskID"))
        token_to_check = toDo.user.token
        if serialized.data.get("token") == token_to_check:
            task_name = toDo.taskID
            task = get_object_or_404(PeriodicTask, name=task_name)
            task.delete()
            toDo.delete()
            return Response({}, status=200)
        else:
            return Response({"message": "This user cannot delete this task"},
                            status=400)
    # serialized = DeleteTaskScheduleSerializer(data=request.data)
    # if serialized.is_valid(raise_exception=True):
    #     name = serialized.data.get("name")
    #     token = serialized.data.get("token")
    #     idt = serialized.data.get("id")
    #     name = str(name) + " " + str(token) + " " + idt
    #     task = get_object_or_404(PeriodicTask, name=name)
    #     task.delete()
    #     return Response({}, status=200)
