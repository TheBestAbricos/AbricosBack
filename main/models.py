from django.db import models


# Create your models here.
class UserInfo(models.Model):
    userID = models.IntegerField()
    taskID = models.IntegerField(null=True, blank =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)