from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    # Get all users except current user
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    if target_username == 'AI_Tutor':
        # Convention for AI chat
        room_name = f'mentor_{request.user.username}'
    else:
        # Convention for P2P chat: sorted usernames
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
