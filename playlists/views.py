from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, Comment
from django.core.paginator import Paginator

# 플레이리스트 메인페이지
def main(request):
    playlists_list = Playlist.objects.all()
    paginator = Paginator(playlists_list,3)
    page = request.GET.get('page')
    playlists = paginator.get_page(page)
    return render(request, 'playlists/main.html', {'playlists': playlists})


# 상세보기페이지
def show(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    return render(request, 'playlists/show.html', {'playlist': playlist})


# 플레이리스트 수정하기
def edit(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    tags = playlist.tags.all()
    content=""
    for tag in tags:
        content += "♬" + str(tag)
    return render(request, 'playlists/edit.html', {"playlist":playlist,'content':content })


def update(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    if request.method =="POST":
        playlist.music = request.POST.get('music')
        playlist.kinds = request.POST.get('kinds')
        playlist.tags = request.POST.get('tags')
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
    if request.method =="POST":
        user = request.user
        if user.is_anonymous:
            return redirect('account_login') #이거 account_login으로 수정해야함 <지금계정이없어서 안됨>
        else:
            playlist = get_object_or_404(Playlist, pk = playlist_id)
            message = request.POST.get('message')
            Comment.objects.create(writer=user, playlist = playlist, message=message)
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
    playlist = get_object_or_404(Playlist, pk = playlist_id)

    is_like = user in playlist.likes.all()

    if is_like:
        playlist.likes.remove(user)
    else:
        playlist.likes.add(user)

    return redirect('playlists:show', playlist_id)


# 검색
def search(request):
    search = request.GET.get('query')
    search_result = Playlist.objects.filter(title__contains=query)
    return render(request, 'playlists/search.html', {'search_result': search_result})

