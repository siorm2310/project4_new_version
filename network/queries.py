from .models import Post,User
from django.shortcuts import get_list_or_404,get_object_or_404
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
    user = get_object_or_404(User,username=username)
    posts = get_list_or_404(Post,creator=user)
    return posts

def add_new_post():
    pass