from django.shortcuts import render
from .models import Game

def index(request):
    game = Game.objects.order_by('?').first()
    return render(request, 'core/index.html', {
        'game': game,
    })