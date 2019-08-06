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
    path('add/', views.add, name="add"),
    path('add_music/', views.add_music, name="add_music"),
]