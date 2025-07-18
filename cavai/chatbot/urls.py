from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('cv/', views.cv_view, name='cv_view'),
    path('vibe-coding/', views.vibe_coding_view, name='vibe_coding_view'),
]