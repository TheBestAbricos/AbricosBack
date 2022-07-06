from django.urls import path, include
from . import views

urlpatterns = [
    path('start/', views.start),
    path('schedule/', views.schedule),
    path('unlinkTelegram/<int:token>/', views.unlinkTelegram),
    path('editSchedule/', views.editSchedule),
    path('deleteSchedule/', views.deleteSchedule),
]