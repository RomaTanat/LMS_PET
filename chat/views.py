
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Message, Room

@login_required
def room(request, room_name):
    # Enforce privacy for mentor rooms
    if room_name.startswith('mentor_'):
        expected_room = f'mentor_{request.user.username}'
        if room_name != expected_room and not request.user.is_superuser:
             return redirect('room', room_name=expected_room)

    room, created = Room.objects.get_or_create(name=room_name, defaults={'slug': room_name})
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50] # Last 50 messages


    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })