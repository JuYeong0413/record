from django.shortcuts import render, redirect, get_object_or_404
from musics.models import Music
from playlists.models import Playlist
from .models import User

# Create your views here.
# 프로필 페이지
def main(request, id):
    user_profile = get_object_or_404(User, pk=id)
    return render(request, 'users/main.html', {'user_profile': user_profile})


# 프로필 수정 페이지
def edit(request, id):
    current_user = request.user
    user = get_object_or_404(User, pk=id)

    if user == current_user:
        return render(request, 'users/edit.html', {'user': user})
    else:
        return redirect('main', id)


# 프로필 수정
def update(request, id):
    if request.method == "POST":
        user = get_object_or_404(User, pk=id)
        username = request.POST.get('username')
        introduction = request.POST.get('introduction')
        user.username = username
        user.introduction = introduction

        if request.FILES.get('image'):
            user.image = request.FILES.get('image')

        user.save()
        return redirect('users:main', id)


# 팔로우, 언팔로우
def follow_toggle(request, id):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
    
    followed_user = get_object_or_404(User, pk=id)

    is_follower = user in followed_user.followers.all()

    if is_follower:
        user.followings.remove(followed_user)
    else:
        user.followings.add(followed_user)

    return redirect('playlists:main')


# 작성한 노래 게시글
def musics(request, id):
    musics = Music.objects.filter(writer__id=id)
    return render(request, 'users/musics.html', {'musics': musics})


# 생성한 플레이리스트 게시글
def playlists(request, id):
    current_user = request.user
    user = get_object_or_404(User, pk=id)

    if user == current_user:
        playlists = Playlist.objects.filter(creator__id=id)
    else:
        playlists = Playlist.objects.filter(creator__id=id, kinds=0)

    return render(request, 'users/playlists.html', {'playlists': playlists})


# 좋아하는 플레이리스트 목록
def likes(request, id):
    current_user = request.user
    user = get_object_or_404(User, pk=id)

    if user == current_user:
        playlists = Playlist.objects.filter(likes=user)
    else:
        playlists = Playlist.objects.filter(likes=user, kinds=0)

    return render(request, 'users/likes.html', {'playlists': playlists})