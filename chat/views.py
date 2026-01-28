
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    """
    Chat lobby: lists all users to start a chat with.
    """
    # Fetch all users except the current one
    # Note: In a real app, you might filter by 'active' or friends only
    all_users = User.objects.exclude(id=request.user.id)

    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    """
    Redirects to a private chat room with the target user.
    Room name is deterministic: sorted(usernames).
    """
    target_user = get_object_or_404(User, username=target_username)

    # Sort usernames to ensure user1+user2 and user2+user1 land in the same room
    participants = sorted([request.user.username, target_user.username])
    room_name = f"{participants[0]}_{participants[1]}"

    return redirect('chat:room', room_name=room_name)

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50] # Last 50 messages


    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })