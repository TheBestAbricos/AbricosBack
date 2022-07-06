from rest_framework import serializers


class TaskScheduleSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    name = serializers.CharField(max_length=3000)
    token = serializers.IntegerField(required=True)


class EditTaskSerializer(serializers.Serializer):
    old_name = serializers.CharField(max_length=3000, required=True)
    new_name = serializers.CharField(max_length=3000, allow_blank=True)
    new_time = serializers.DateTimeField(allow_null=True)
    token = serializers.IntegerField(required=True)


class DeleteTaskScheduleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=3000)
    token = serializers.IntegerField(required=True)