from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('cv/', views.cv_view, name='cv_view'),
]