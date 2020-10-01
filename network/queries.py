from .models import Post,User

def get_followers(User):
    pass

def get_all_posts(User):
    return User.objects.all()

def get_follows_posts(User):
    pass