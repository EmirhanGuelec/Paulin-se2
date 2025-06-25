import os, json
from meine_app.backend.registrierung_login import registrierung as mod_registrierung
from meine_app.backend.registrierung_login import login as mod_login
from meine_app.backend.registrierung_login.pruefung import check_login
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User

USER_JSON_PATH = os.path.join(settings.BASE_DIR, 'meine_app', 'backend', 'registrierung_login', 'users.json')

@check_login
def startseite(request):
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/index.html", {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        "username": username,
        "password": password
    })

@check_login
def create_post(request):
    username = request.GET.get("username")
    password = request.GET.get("password")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = username
            post.save()
            return redirect(f'/startseite?username={username}&password={password}')
    else:
        form = PostForm()

    return render(request, "meine_app/posten.html", {
        'post_form': form,
        'username': username,
        'password': password,
    })


@check_login
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.GET.get("username")  # <- statt request.user
            comment.post = post
            comment.save()
    return redirect(f'/startseite?username={request.GET.get("username")}&password={request.GET.get("password")}')

@check_login
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = request.GET.get("username")

    like, created = Like.objects.get_or_create(post=post, username=username)
    if not created:
        like.delete()
    return redirect(f'/startseite?username={username}&password={request.GET.get("password")}')

def register(request):
    return mod_registrierung.registrieren(request, USER_JSON_PATH)

def login_check(request):
    return mod_login.login_check(request, USER_JSON_PATH)

def saveUploadedFile(request):
    if request.method == "POST" and request.FILES.get("datei"):
        datei = request.FILES["datei"]
        FileSystemStorage("/var/www/static/dateien/").save(datei.name, datei)
    return render(request, "meine_app/template.html")

@check_login
def profilseite(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/Profil.html", {"username": username, "password": password})

@check_login
def chat(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/chat.html", {"username": username, "password": password})

@check_login
def freunde(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/freunde.html", {"username": username, "password": password})


def impressum(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/impressum.html", {"username": username, "password": password})

def login(request):
    return render(request, "meine_app/login.html")

@check_login
def posten(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    form = PostForm()

    if request.method == "POST" and request.FILES.get("datei"):
        datei = request.FILES["datei"]
        FileSystemStorage("/var/www/static/dateien/").save(datei.name, datei)
       

    return render(request, "meine_app/posten.html", {
        "username": username,
        "password": password,
        "post_form": form
    })


def registrierung(request):
    return render(request, "meine_app/registrierung.html")

@check_login
def suche(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    query = request.GET.get('q')
    users = []

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, "meine_app/suche.html",
        {
            "username": username,
            "password": password,
            "users": users,
            "query": query,
        }
    )

#def suche(request):
 #   username = request.GET.get("username")
  #  password = request.GET.get("password")
   # return render(request, "meine_app/suche.html", {"username": username, "password": password})

@check_login
def einstellungen(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/einstellungen.html", {"username": username, "password": password})
