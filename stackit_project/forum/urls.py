from django.urls import path
from . import views

urlpatterns = [
    path('question/<int:pk>/delete/', views.delete_question, name='delete_question'),

    path('', views.home, name='home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
]
# This file defines the URL patterns for the forum application.
# It includes paths for the home page, asking a question, and viewing question details.