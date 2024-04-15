#системa уведомлений

from django import forms

class NotificationPreferencesForm(forms.ModelForm):
    class Meta:
        model = NotificationPreferences
        fields = ['event_type', 'notification_method']


#Электронный дневник
from .models import Grade


class CommentForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['teacher_comment']


# Интеграция с родительским порталом: