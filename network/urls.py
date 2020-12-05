
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_posts, name="following_posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("likes/<int:post_id>", views.likes_api, name="likes_api"),
    path("edit/<int:post_id>", views.edit_api, name="edit_api"),
]
