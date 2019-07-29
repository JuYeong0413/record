from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('<int:id>/', views.main, name="main"),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('update/<int:id>/', views.update, name="update"),
    path('follow_toggle/<int:id>/', views.follow_toggle, name="follow_toggle"),
    path('<int:id>/musics/', views.musics, name="musics"),
    path('<int:id>/playlists/', views.playlists, name="playlists"),
    path('<int:id>/likes/', views.likes, name="likes"),
]