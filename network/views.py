import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse,
                         request)
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, User
from .queries import *


def index(request):
    posts = get_all_posts()
    if request.method == "POST":
        user = request.user

        if 'addPost' in request.POST:
            title = request.POST["title"]
            content = request.POST["content"]
            if title is not None and content is not None:
                add_new_post(user,title,content)
        
         
        return render(request, "network/index.html", {"posts": posts, "user": request.user})
    return render(request, "network/index.html", {"posts": posts, "user": request.user})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def following_posts(request):
    posts = get_follows_posts(request.user)
    return render(request, "network/index.html", {"posts": posts, "user": request.user})


def profile(request, username):
    posts = get_user_posts(username)
    is_followed = is_user_followed(request.user, username)

    if request.method == "POST":
        action = request.POST["follow_btn"]
        if action == "follow":
            follow_user(request.user, username)
        else:
            unfollow_user(request.user, username)
        is_followed = not is_followed
        return render(request, "network/profile.html",
                      {"posts": posts, "user": request.user, "username": username, "is_followed": is_followed})
    return render(request, "network/profile.html",
                  {"posts": posts, "user": request.user, "username": username, "is_followed": is_followed})


@csrf_exempt
def likes_api(request, post_id):
    if request.method == "GET":
        like_status = get_like_status(request.user, post_id)
        return JsonResponse({"post_id": post_id, "liked": like_status[0], "current_num_likes": like_status[1]})

    if request.method == "POST":
        payload = json.loads(request.body)
        if payload["liked"]:
            add_like(request.user, post_id)
            like_status = get_like_status(request.user, post_id)
            return JsonResponse({"post_id": post_id, "like_change": "success", "liked": True, "liked": like_status[0], "current_num_likes": like_status[1]})
        remove_like(request.user, post_id)
        like_status = get_like_status(request.user, post_id)
        return JsonResponse({"post_id": post_id, "like_change": "success", "liked": False, "liked": like_status[0], "current_num_likes": like_status[1]})

@csrf_exempt
def edit_api(request,post_id):
    user = request.user
    if request.method == "POST":
        if 'editPost' in request.POST:
            title = request.POST["edit_title"]
            content = request.POST["edit_content"]
            if title is not None and content is not None:
                edit_post(post_id,user,title,content)
                return redirect('profile',user.username)
