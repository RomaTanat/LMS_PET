from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    # Get all users excluding the current user
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    target_user = get_object_or_404(User, username=target_username)

    # Check if this is an AI chat request (optional, depending on how AI is handled)
    # The existing template seemed to hardcode 'AI_Tutor', but let's stick to user logic first.

    # Deterministic room name for 1-on-1 chat
    users = sorted([request.user.username, target_user.username])
    room_name = f"{users[0]}_{users[1]}"

    return redirect('room', room_name=room_name)

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50] # Last 50 messages

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })
