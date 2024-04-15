#системa уведомлений
from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    notification_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)


#Электронный дневник
from django.contrib.auth.models import User

class Grade(models.Model):
    # Поля модели оценок
    ...
    teacher_comment = models.TextField(blank=True)


# Интеграция с родительским порталом:
class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Дополнительные поля для родителей, если нужно

class Student(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    # Поля модели для информации о