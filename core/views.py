from django.shortcuts import render
# from .models import Game
from .functions import query

def index(request):
    # game = Game.objects.order_by('?').first()

    game = query()
    
    return render(request, 'core/index.html', {
        'game': game,
    })