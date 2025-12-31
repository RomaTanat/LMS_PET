from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('start/<str:target_username>/', views.start_private_chat, name='start_private_chat'),
    path('<str:room_name>/', views.room, name='room'),
]