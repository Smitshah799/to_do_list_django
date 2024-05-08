from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/<str:pk>", views.homepage, name="homepage"),
    path("adminhome/<str:pk>", views.adminhomepage, name="admin_homepage"),
    path("login/", views.loginuser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("signup/", views.registeruser, name="signup"),
    path("delete_note/<int:note_id>/", views.delete_note, name="delete_note"),
]
