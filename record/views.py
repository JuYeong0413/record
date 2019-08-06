from django.shortcuts import render
from playlists.models import Playlist

# Create your views here.
def main(request):
	playlists = Playlist.objects.all()[:3]

	return render(request, 'main.html', {'playlists': playlists})