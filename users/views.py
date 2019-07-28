from django.shortcuts import render, redirect, get_object_or_404
from .models import User

def follow_toggle(request, id):
    user = request.user
    if user.is_anonymous:
        return redirect('account_login')
    
    followed_user = get_object_or_404(User, pk =id)

    is_follower = user in followed_user.followers.all()

    if is_follower:
        user.followings.remove(followed_user)
    else:
        user.followings.add(followed_user)

    return redirect('playlists:main')
