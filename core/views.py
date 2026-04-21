from django.shortcuts import render

from core.models import Room


# Create your views here.
def index(request):

    context = {
        'rooms': Room.objects.all()
    }
    return render(request, 'index.html', context)