from .models import Post, User
from django.shortcuts import get_list_or_404, get_object_or_404


def get_follows_posts(user):
    posts = []
    try:
        follows = user.follows.all()
        for followee in follows:
            posts.append(Post.objects.get(creator=followee))
        return posts
    except:
        return None


def get_all_posts(User):
    return User.objects.all()


def get_user_posts(username):
    user = get_object_or_404(User, username=username)
    posts = get_list_or_404(Post, creator=user)
    return posts


def add_new_post():
    pass


def is_user_followed(user, user_to_follow):
    user = get_object_or_404(User, username=user)

    if user.follows.filter(username=user_to_follow).exists():
        return True
    return False


def follow_user(user, user_to_follow):
    user_object = User.objects.get(username=user_to_follow)
    user.follows.add(user_object)
    user.save()


def unfollow_user(user, user_to_follow):
    user_object = User.objects.get(username=user_to_follow)
    user.follows.remove(user_object)
    user.save()


def add_like(user, post):
    pass
