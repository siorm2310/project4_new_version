from .models import Post, User
from django.shortcuts import get_list_or_404, get_object_or_404
from django.utils.timezone import now

def get_follows_posts(user):
    posts = Post.objects.none() # union of all querysets
    try:
        follows = user.follows.all()
        for followee in follows:
            followee_posts = Post.objects.filter(creator=followee)
            posts = posts.union(followee_posts)
        posts.order_by("-time")
        return posts
    except:
        return None


def get_all_posts():
    return Post.objects.all().order_by('-time')


def get_user_posts(username):
    user = get_object_or_404(User, username=username)
    posts = get_list_or_404(Post.objects.order_by('-time'), creator=user)
    return posts


def add_new_post(creator,title,content):
    new_post = Post(creator=creator,title=title,content=content)
    new_post.save()
    return

def edit_post(post_id,creator,title,content):
    post = get_object_or_404(Post,id=post_id)
    if post.creator == creator:
        post.title = title
        post.content = content
        post.time = now()
        post.save()

def is_user_followed(user, user_to_follow):
    if user.id is None:
        return False

    user = User.objects.get(username=user)

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


def get_like_status(user, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_liked = post.likes.filter(username=user).exists()
    current_likes = post.get_num_of_likes()
    return [is_liked, current_likes]


def add_like(username, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(username=username)
    post.likes.add(user)


def remove_like(username, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(username=username)
    post.likes.remove(user)
