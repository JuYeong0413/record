from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, Comment
from musics.models import Music
from django.core.paginator import Paginator

# 플레이리스트 메인페이지
def main(request):
    playlists_list = Playlist.objects.all().order_by('-id')
    paginator = Paginator(playlists_list, 10)
    page = request.GET.get('page')
    playlists = paginator.get_page(page)
    return render(request, 'playlists/main.html', {'playlists': playlists})


# 상세보기페이지
def show(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    return render(request, 'playlists/show.html', {'playlist': playlist})


# 플레이리스트 수정하기
def edit(request, id):
    user = request.user
    playlist = get_object_or_404(Playlist, pk=id)

    if user == playlist.creator:
        tags = playlist.tags.all()
        content = ""
        for tag in tags:
            content += "♬" + str(tag)
        return render(request, 'playlists/edit.html', {"playlist": playlist, 'content': content })
    else:
        return redirect('playlists:show', id)


def update(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    if request.method == "POST":
        playlist.music = request.POST.get('music')
        playlist.kinds = request.POST.get('kinds')
        playlist.tags = request.POST.get('tags')
        
        if request.FILES.get('cover'):
            playlist.cover = request.FILES.get('cover')

        playlist.title = request.POST.get('title')
        
        if playlist.kinds == "public":
            playlist.kinds = 0
        else:
            playlist.kinds = 1

        playlist.save()
    return redirect('playlists:show', id)


# 플레이리스트 삭제하기
def delete(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    playlist.delete()
    return redirect('playlists:main')


# 댓글생성
def create_comment(request, playlist_id):
    if request.method == "POST":
        user = request.user
        if user.is_anonymous:
            return redirect('account_login')
        else:
            playlist = get_object_or_404(Playlist, pk=playlist_id)
            message = request.POST.get('message')
            Comment.objects.create(writer=user, playlist=playlist, message=message)
            return redirect('playlists:show', playlist_id)


# 댓글삭제
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    playlist_id = comment.playlist.id
    comment.delete()
    return redirect('playlists:show', playlist_id)


# 좋아요
def like_toggle(request, playlist_id):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
    playlist = get_object_or_404(Playlist, pk=playlist_id)

    is_like = user in playlist.likes.all()

    if is_like:
        playlist.likes.remove(user)
    else:
        playlist.likes.add(user)

    return redirect('playlists:show', playlist_id)


#태그 검색
def tag(request, playlist_id, tag_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    tag = playlist.tags.get(pk=tag_id)
    sorted_playlists = Playlist.objects.filter(tags__name__in=[tag])
    return render(request, 'playlists/tag.html', {'sorted_playlists':sorted_playlists})

#음악삭제하기
def delete_music(request, playlist_id, music_id):
    playlist = get_object_or_404(Playlist, pk = playlist_id)
    music = playlist.musics.get(pk=music_id)
    music.delete()
    return redirect('playlists:show', playlist_id)

# 검색
def search(request):
    query = request.GET.get('query')
    search_list = Playlist.objects.filter(title__contains=query)
    paginator = Paginator(search_list, 10)
    page = request.GET.get('page')
    search_result = paginator.get_page(page)
    return render(request, 'playlists/search.html', {'search_result': search_result, 'search_list':search_list})


#새 플레이리스트 생성
def new(request):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')

    if request.method == "POST":
        playlist = Playlist()
        playlist.creator = user
        playlist.title = request.POST.get('title')
        playlist.description = request.POST.get('description')
        playlist.tags = request.POST.get('tags')
        playlist.kinds = request.POST.get('kinds')

        if request.FILES.get('cover'):
            playlist.cover = request.FILES.get('cover')

        if playlist.kinds == "public":
            playlist.kinds = 0
        else:
            playlist.kinds = 1
        
        playlist.save()

        music_id = request.POST.get('music_id')
        music = Music.objects.get(pk=music_id)
        playlist.musics.add(music)
        
        return redirect('playlists:show', playlist.id)
    else:
        return render(request,'playlists/new.html')

    


