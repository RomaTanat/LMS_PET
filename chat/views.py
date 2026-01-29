
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    """
    Chat lobby: Lists all users to start a chat with.
    """
    # Exclude current user and potentially inactive users if needed
    all_users = User.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    """
    Creates or redirects to a deterministic 1-on-1 chat room.
    Room name format: 'user1_user2' (sorted alphabetically)
    """
    target_user = get_object_or_404(User, username=target_username)

    # Deterministic room name
    users = sorted([request.user.username, target_user.username])
    room_name = f"{users[0]}_{users[1]}"

    return redirect('chat:room', room_name=room_name)

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50] # Last 50 messages


    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })
