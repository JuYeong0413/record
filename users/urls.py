from django.urls import path
from . import views

app_name = "users"
urlpatterns = [
    path('follow_toggle/<int:id>/', views.follow_toggle, name="follow_toggle"),
]