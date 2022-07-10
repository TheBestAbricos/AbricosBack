from django.db import models


# Create your models here.
class UserInfo(models.Model):
    userID = models.IntegerField()
    token = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Task(models.Model):
    taskID = models.CharField(max_length=256)
    user = models.ForeignKey(UserInfo, blank=True, on_delete=models.CASCADE)
    description = models.TextField()
    time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
