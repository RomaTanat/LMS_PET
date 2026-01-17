from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='chat_index'),
    path('start_chat/<str:target_username>/', views.start_private_chat, name='start_private_chat'),
    path('<str:room_name>/', views.room, name='room'),
]
