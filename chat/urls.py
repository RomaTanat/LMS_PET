from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Lobby view
    path('', views.index, name='index'),

    # Start private chat
    path('start/<str:target_username>/', views.start_private_chat, name='start_private_chat'),

    # Room view (must be last to avoid matching other patterns)
    path('<str:room_name>/', views.room, name='room'),
]
