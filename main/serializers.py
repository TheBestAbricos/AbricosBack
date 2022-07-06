from rest_framework import serializers


class TaskScheduleSerializer(serializers.Serializer):
    time = serializers.DateTimeField()
    description = serializers.CharField(max_length=3000)
    userID = serializers.IntegerField(required=True)

