from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    """
    Chat Lobby: Lists all users except the current one.
    """
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/rooms.html', {
        'all_users': users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    """
    Initiates a 1-on-1 chat.
    Room name is deterministic: sorted usernames joined by underscore.
    """
    # Special case for AI Tutor
    if target_username == 'AI_Tutor':
        room_name = f'mentor_{request.user.username}'
        return redirect('chat:room', room_name=room_name)

    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        return redirect('chat:index')

    # Sort usernames to ensure room_name is always "userA_userB"
    participants = sorted([request.user.username, target_username])
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
