from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog.models import MyUser, Post, Like, Comment, Follow


@login_required(login_url='/login/')
def home_view(request):
    user = MyUser.objects.filter(user=request.user).first()
    users = MyUser.objects.exclude(user=request.user)
    following_users = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
    posts = Post.objects.filter(author_id__in=list(following_users) + [user]).order_by('-created_at')
    likes = Like.objects.all()
    comments = Comment.objects.all()
    for post in posts:
        post.comments = comments.filter(post_id=post.id)
    d = {
        'posts': posts,
        'users': users[:5],
        'user': user,
        'likes': likes,
        'comments': comments[:10]
    }
    return render(request, 'index.html', context=d)


def login_view(request):
    d = {}
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            d['error'] = 'Invalid username or password'

    return render(request, 'signin.html', context=d)


def signup_view(request):
    d = {}
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password1 = data["password1"]
        password2 = data["password2"]
        if User.objects.filter(username=username).exists():
            d['error'] = 'Username already exists'
        elif password1 != password2:
            d['error'] = 'Passwords do not match'
        else:
            user = User.objects.create(username=username, password=make_password(password1))
            user.save()
            my_user = MyUser.objects.create(user=user)
            my_user.save()
            return redirect('/login')
    return render(request, 'signup.html', context=d)


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='/login')
def post_upload_view(request):
    if request.method == "POST":
        my_user = MyUser.objects.filter(user=request.user).first()
        post = Post.objects.create(post_image=request.FILES['post_image'], author=my_user)
        post.save()
        my_user.post_count += 1
        my_user.save(update_fields=['post_count'])
        return redirect('/')
    return redirect('/')


@login_required(login_url='/login')
def like_view(request):
    if request.method == "POST":
        data = request.POST
        print(data)
        post_id = data['post_id']
        author = MyUser.objects.filter(user=request.user).first()
        liked = Like.objects.filter(author=author, post_id=post_id)
        post = Post.objects.filter(id=post_id).first()
        if liked:
            liked.delete()
            post.like_count -= 1
            post.save(update_fields=['like_count'])
        else:
            like = Like.objects.create(author=author, post_id=post_id)
            like.save()
            post.like_count += 1
            post.save(update_fields=['like_count'])
        return redirect('/#{}'.format(post_id))
    return render(request, 'index.html')


@login_required(login_url='/login')
def follow_view(request):
    user_id = request.GET.get('user_id')
    my_user = MyUser.objects.filter(user=request.user).first()
    follow_count = MyUser.objects.filter(id=user_id).first()
    followed = Follow.objects.filter(follower=my_user, following_id=user_id)
    if not followed:
        follow = Follow.objects.create(follower=my_user, following_id=user_id)
        follow.save()
        follow_count.follower_count += 1
        follow_count.save(update_fields=['follower_count'])
        my_user.following_count += 1
        my_user.save(update_fields=['following_count'])
    else:
        followed.delete()
        follow_count.follower_count -= 1
        follow_count.save(update_fields=['follower_count'])
        my_user.following_count -= 1
        my_user.save(update_fields=['following_count'])
    return redirect('/')


@login_required(login_url='/login')
def comment_view(request):
    if request.method == 'POST':
        data = request.POST
        message = data["message"]
        post_id = data["post_id"]
        author = MyUser.objects.filter(user=request.user).first()
        obj = Comment.objects.create(message=message, post_id=post_id, author=author)
        post = Post.objects.filter(id=post_id).first()
        obj.save()
        post.comment_count += 1
        post.save(update_fields=['comment_count'])
        return redirect('/#{}'.format(post_id))
    return render(request, 'index.html')


@login_required(login_url='/login')
def setting_view(request):
    my_user = MyUser.objects.filter(user=request.user).first()
    d = {
        'my_user': my_user
    }
    if request.method == "POST":
        data = request.POST
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']
        about = data['about']
        relationship = data['relationship']
        location = data['location']
        working_at = data['working_at']

        my_user.first_name = first_name
        my_user.last_name = last_name
        my_user.email = email
        my_user.about_me = about
        my_user.relationship = relationship
        my_user.location = location
        my_user.working_at = working_at
        my_user.save(update_fields=['first_name', 'last_name', 'email', 'about_me',
                                    'relationship', 'location', 'working_at'])
        return redirect('/setting', context=d)
    return render(request, 'setting.html', context=d)


@login_required(login_url='/login')
def profile_view(request):
    user_id = request.GET.get('user_id')
    user = MyUser.objects.filter(user_id=user_id).first()
    current_user = MyUser.objects.filter(user=request.user).first()
    posts = Post.objects.filter(author=user)
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    if user == current_user:
        actual_user = True
    else:
        actual_user = False
    d = {
        "user": user,
        "actual_user": actual_user,
        "posts": posts,
        "post_count": posts.count(),
        "following_count": following_count,
        "follower_count": follower_count,
    }
    return render(request, 'profile.html', context=d)


def profile_image_view(request):
    if request.method == "POST":
        my_user = MyUser.objects.filter(user=request.user).first()
        my_user.user_photo = request.FILES['user_photo']
        my_user.save(update_fields=['user_photo',   ])
    return redirect('/profile?user_id={}'.format(my_user))
