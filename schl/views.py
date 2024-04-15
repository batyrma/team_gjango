#системa уведомлений
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Exam, Notification
from .forms import NotificationPreferencesForm

# Логика отправки уведомлений
def send_notification(user, text, notification_type):
    Notification.objects.create(user=user, text=text, notification_type=notification_type)

# Обновление настроек уведомлений
@login_required
def update_notification_preferences(request):
    if request.method == 'POST':
        form = NotificationPreferencesForm(request.POST, instance=request.user.notificationpreferences)
        if form.is_valid():
            form.save()
            return render(request, 'success.html')  # Отобразить страницу с сообщением об успешном обновлении настроек
    else:
        form = NotificationPreferencesForm(instance=request.user.notificationpreferences)
    return render(request, 'notification_preferences.html', {'form': form})

# Представление для отправки уведомлений о предстоящем экзамене
@login_required
def exam_notification_view(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    students = exam.lesson.students.all()
    for student in students:
        send_notification(student.user, f"Предстоящий экзамен по {exam.lesson.name} {exam.date_time}", "exam")


#Электронный дневник
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Grade
from .forms import CommentForm


@login_required
def electronic_diary_view(request):
    if request.user.userprofile.userType == UserProfile.STUDENT:
        grades = Grade.objects.filter(student=request.user)
    elif request.user.userprofile.userType == UserProfile.PARENT:
        grades = Grade.objects.filter(student__parent=request.user)
    elif request.user.userprofile.userType == UserProfile.TEACHER:
        grades = Grade.objects.filter(teacher=request.user)
    else:
        grades = Grade.objects.none()

    return render(request, 'electronic_diary.html', {'grades': grades})


@login_required
def add_comment(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            return redirect('electronic_diary')
    else:
        form = CommentForm(instance=grade)
    return render(request, 'add_comment.html', {'form': form, 'grade': grade})


 #Интеграция с родительским порталом:
from .models import Parent, Student, Attendance


def parent_portal(request):
    parent = Parent.objects.get(user=request.user)
    children = Student.objects.filter(parent=parent)

    children_info = []
    for child in children:
        # Получаем информацию о успехах ребенка
        grades = Grade.objects.filter(student=child)
        # Получаем информацию о посещаемости ребенка
        attendance = Attendance.objects.filter(student=child)

        children_info.append({
            'child': child,
            'grades': grades,
            'attendance': attendance,
            # Другая информация о ребенке, если нужно
        })

    return render(request, 'parent_portal.html', {'parent': parent, 'children_info': children_info})
