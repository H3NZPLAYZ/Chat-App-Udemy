from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from core.models import Room


# Create your views here.
@login_required
def index(request):

    context = {
        'rooms': Room.objects.all()
    }
    return render(request, 'index.html', context)

@login_required
def room(request, room_slug):
    room = get_object_or_404(Room, slug=room_slug)

    context = {
        'room': room
    }

    return render(request, 'room.html', context)