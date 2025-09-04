from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    # pick the post you always want to display first
    featured_post = Post.objects.filter(title="Welcome to Mountains 👋👋").first()

    # show all other posts except the featured one
    if featured_post:
        posts = Post.objects.exclude(id=featured_post.id).order_by('-posted_date')
    else:
        posts = Post.objects.all().order_by('-posted_date')

    context = {
        'featured_post': featured_post,
        'posts': posts
    }
    return render(request, 'app1/home.html', context)

def login_view(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Check username or password')
            return redirect('login')
        
    return render(request, 'app1/login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cnfpassword = request.POST.get('cnfpassword')
        
        if password != cnfpassword:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")  # back to form
                
        if not User.objects.filter(username=username).exists():
            newuser = User.objects.create_user(username=username, email=email, password=password)
            newuser.save()
            login(request,newuser)
        else:
            # handle duplicate username
            messages.error(request, 'User already Exists')
            return redirect('signup')
        return redirect('home')
    return render(request, 'app1/signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def newpost(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        post = Post(title=title, content=content, author=request.user)
        post.save()
        return redirect('myblogs')
    context = {}
    return render(request, 'app1/newpost.html', context)

def myblogs(request):
    
    posts = Post.objects.filter(author = request.user).order_by('-posted_date')  
    context = {'posts': posts}
    return render(request, 'app1/myblogs.html', context)

def editblog(request, pk):
    blog = Post.objects.get(pk=pk)
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.content = request.POST.get('content')
        blog.save()
        return redirect('myblogs')
    context = {'title': blog.title, 'content':blog.content}
    return render(request, 'app1/editblog.html', context)

def delete_blog(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == "POST":
        post.delete()
        return redirect("myblogs")