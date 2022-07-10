from rest_framework import serializers

from main.models import Task


class TaskScheduleSerializer(serializers.ModelSerializer):
    token = serializers.IntegerField()

    class Meta:
        model = Task
        fields = ["token", "description", "time", "taskID"]


# class EditTaskSerializer(serializers.Serializer):
#     old_name = serializers.CharField(max_length=3000, required=True)
#     id = serializers.CharField(max_length= 256)
#     new_name = serializers.CharField(max_length=3000, allow_blank=True)
#     new_time = serializers.DateTimeField(allow_null=True)
#     token = serializers.IntegerField(required=True)


class DeleteTaskScheduleSerializer(serializers.Serializer):
    token = serializers.IntegerField(required=True)
    taskID = serializers.CharField(max_length=256)
