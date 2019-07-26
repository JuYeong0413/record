from django.shortcuts import render
from .models import Playlist

def main(request):
    playlists = Playlist.objects.all()
    return render(request, 'main.html', {'playlists':playlists})
