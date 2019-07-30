from django.urls import path
from . import views

app_name = "musics"
urlpatterns = [
 path('', views.main, name="main"),
 path('show/<int:music_id>/', views.show, name="show"),
 path('new/', views.new, name="new" ),
 path('create/',views.create, name="create"),
 path('delete/<int:music_id>/', views.delete, name="delete"),
 path('edit/<int:music_id>/', views.edit, name="edit"),
 path('update/<int:music_id>/', views.update, name="update"),
 path('search/', views.search, name="search"),
 path('show_playlists/', views.show_playlists, name="show_playlists"),
 path('add_music/<int:playlist_id>/', views.add_music, name="add_music"),
]