from django.shortcuts import render, redirect, get_object_or_404
from .models import Playlist, Comment

# 플레이리스트 메인페이지
def main(request):
    playlists = Playlist.objects.all()
    return render(request, 'playlists/main.html', {'playlists': playlists})


# 상세보기페이지
def show(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    return render(request, 'playlists/show.html', {'playlist':playlist})


# 플레이리스트 수정하기
# def edit(request, id):
#     playlists = get_object_or_404(Playlist, pk = id)
#     return render(request, 'playlists/edit.html', {"playlists":playlists})

def update(request, id):
    playlist = get_object_or_404(Playlist, pk=id)
    if request.method =="POST":
        playlist.music = request.POST.get('music')
        playlist.kinds = request.POST.get('kinds')
        playlist.tags = request.POST.get('tags')
        playlist.cover = request.POST.get('cover')
        playlist.title = request.POST.get('title')
        playlist.save()

    return redirect('playlists:show')


# 플레이리스트 삭제하기
def delete(request, id):
    playlist = get_object_or_404(Playlist, pk = id)
    playlist.delete()
    return redirect('playlists:show')


# 댓글보기
def show_comment(request, playlist_id):
    comments = get_object_or_404(Comment, pk = playlist_id)
    return render(request,'playlists/show.html', {'comments':comments})


# 댓글생성
def create_comment(request, playlist_id):
    if request.method =="POST":
        user = request.user
        if user.is_anonymous:
            return redirect('playlists:main')#이거 account_login으로 수정해야함<지금계정이없어서 안됨>
        playlist = get_object_or_404(Playlist, pk = playlist_id)
        message = request.POST.get('message')
        Comment.objects.create(writer=user, playlist = playlist, message=message)
        return redirect('playlists:show/playlist_id' )


# 댓글삭제
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('playlists:show/comment_id')

# 검색
def search(request):
    search = request.GET.get('search')
    search_result = Playlist.objects.filter(title_contains=search)
    return render(request, 'playlists/search.html', {'search_result':search_result})