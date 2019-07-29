from django.shortcuts import render, redirect, get_object_or_404
from .models import Music
from django.core.paginator import Paginator

# Create your views here.
# 노래 메인 페이지
def main(request):
    music_list = Music.objects.all()
    paginator = Paginator(music_list, 10)
    page = request.GET.get('page')
    musics = paginator.get_page(page)
    return render(request, 'musics/main.html', {'musics': musics})
   

# 노래 게시글 상세보기
def show(request, music_id):
    music = get_object_or_404(Music, id=music_id) 
    return render(request, 'musics/show.html', {'music': music})


# 노래 게시글 작성 페이지
def new(request):
    return render(request, 'musics/new.html')


# 노래 게시글 작성
def create(request):
    user = request.user
    if request.method =="POST":
        music = Music()
        music.writer = user
        music.title = request.POST.get('title')
        music.singer = request.POST.get('singer')
        music.link = request.POST.get('link')
        music.save()

    return redirect('musics:main')


# 노래 게시글 수정
def update(request, music_id):
    if request.method == "POST":
        music = get_object_or_404(Music, pk=music_id)
        music.title = request.POST.get('title')
        music.singer = request.POST.get('singer')
        music.link = request.POST.get('link')
        music.save()

    return redirect('musics:show', music_id)


# 노래 게시글 삭제
def delete(request, music_id):
    get_object_or_404(Music, pk=music_id).delete()
    return redirect('musics:main')


# 노래 게시글 수정 페이지
def edit(request, music_id):
    music = get_object_or_404(Music, pk=music_id)
    return render(request, 'musics/edit.html', {'music': music})


# 노래 검색
def search(request):
    query = request.GET.get('query')
    search_result = Music.objects.filter(title__contains=query)
    return render(request,'musics/search.html', {'search_result': search_result})