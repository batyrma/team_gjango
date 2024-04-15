
from django.urls import path
from . import views


urlpatterns = [
    #Электронный дневник
    path('electronic_diary/', views.electronic_diary_view, name='electronic_diary'),
    path('add_comment/<int:grade_id>/', views.add_comment, name='add_comment'),
    # Интеграция с родительским порталом:
    path('parent_portal/', views.parent_portal, name='parent_portal'),
]