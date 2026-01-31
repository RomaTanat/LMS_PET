from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    """
    Renders the chat lobby with a list of users.
    """
    all_users = User.objects.exclude(pk=request.user.pk)
    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    """
    Initiates a private chat by redirecting to a unique room for the two users.
    """
    target_user = get_object_or_404(User, username=target_username)

    # Create a consistent room name based on sorted usernames
    # This ensures user1 and user2 always end up in "user1_user2" regardless of who starts it
    users = sorted([request.user.username, target_user.username])
    room_name = f"{users[0]}_{users[1]}"

    return redirect('chat:room', room_name=room_name)

@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50] # Last 50 messages

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages,
        'user': request.user
    })
