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
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import *
from rest_framework.response import Response
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from . import tasks
from main.models import *
from main.serializers import *
from .utils import *
