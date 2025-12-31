
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def rooms_list(request):
    """
    Renders the list of available users for chat.
    """
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'chat/rooms.html', {
        'all_users': users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    """
    Redirects to a private chat room with the target user.
    """
    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        # Handle case where user does not exist
        return redirect('chat:rooms_list')

    # Sort usernames to ensure consistent room name regardless of who starts the chat
    users = sorted([request.user.username, target_username])
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