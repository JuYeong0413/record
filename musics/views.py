from django.shortcuts import render, redirect, get_object_or_404
from .models import Music

# Create your views here.
    
def main(request):
    musics = Music.objects.all()
    return render(request, 'musics/main.html', {'musics':musics})
   

def show(request, music_id):
    music = get_object_or_404(Music, id=music_id) 
    return render(request, 'musics/show.html', {'music':music})

def new(request):
    return render(request, 'musics/new.html')

def create(request):
    if request.method =="POST":
        music = Music()
        music.title = request.GET['title']
        music.writer =  request.GET['writer']
        music.singer = request.GET['singer']
        music.genre = request.GET['genre']
        music.lyrics = request.GET['lyrics']
        music.link = request.GET['link']
        music.save()
    return redirect('musics/main.html')


def update(request, music_id):
    if request.method == "POST":
        music = get_object_or_404(Music, pk=music_id)
        music.title = request.GET['title']
        music.writer = request.GET['writer']
        music.singer = request.GET['singer']
        music.lyrics = request.GET['lyrics']
        music.genre = request.GET['genre']
        
        music.save()

    return redirect('musics/main.html')


def delete(request, music_id):
    get_object_or_404(Music, pk=music_id).delete()
    return redirect('musics/main.html')

def edit( request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    return render(request, 'musics/edit.html', {'music':music})

def search(request):
    search = request.GET.get('search')
    search_result = Music.objects.filter(title__contains=search)
    return render(request,'musics/search.html', {'search_result':search_result})