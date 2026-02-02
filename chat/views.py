from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message, Room

User = get_user_model()

@login_required
def index(request):
    """
    Chat Lobby: List all users and AI Tutor.
    """
    # Create AI Tutor if not exists
    ai_tutor, created = User.objects.get_or_create(username='AI_Tutor', defaults={'email': 'ai@lms.local'})
    if created:
        ai_tutor.set_unusable_password()
        ai_tutor.save()

    all_users = User.objects.exclude(id=request.user.id).order_by('username')
    return render(request, 'chat/rooms.html', {
        'all_users': all_users,
        'current_user': request.user
    })

@login_required
def start_private_chat(request, target_username):
    if target_username == 'AI_Tutor':
        room_name = f'mentor_{request.user.username}'
        return redirect('chat:room', room_name=room_name)

    target_user = get_object_or_404(User, username=target_username)

    # Sort usernames to ensure consistent room name for both participants
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
