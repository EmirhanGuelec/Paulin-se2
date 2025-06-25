import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm, ProfileForm
from meine_app.backend.registrierung_login.pruefung import check_login
from meine_app.backend.registrierung_login import registrierung as mod_registrierung
from meine_app.backend.registrierung_login import login as mod_login
from django.urls import reverse

USER_JSON_PATH = os.path.join(
    settings.BASE_DIR,
    'meine_app',
    'backend',
    'registrierung_login',
    'users.json'
)

@check_login
def startseite(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    posts = Post.objects.all().order_by('-created_at')
    post_form = PostForm()
    comment_form = CommentForm()
    liked_posts = list(
        Like.objects.filter(username=username, post__in=posts)
            .values_list('post_id', flat=True)
    )
    return render(request, "meine_app/index.html", {
        'posts': posts,
        'post_form': post_form,
        'comment_form': comment_form,
        'username': username,
        'password': password,
        'liked_posts': liked_posts,
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
            comment.author = request.GET.get("username")
            comment.post = post
            comment.save()
    return redirect(f'/startseite?username={request.GET.get("username")}&password={request.GET.get("password")}')

@check_login
def toggle_like_ajax(request):
    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Nur AJAX-POST erlaubt"}, status=400)
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    user = request.GET.get("username")
    like, created = Like.objects.get_or_create(post=post, username=user)
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({"liked": liked, "count": post.likes.count()})

@check_login
def add_comment_ajax(request):
    if request.method != "POST" or request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return JsonResponse({"error": "Nur AJAX-POST erlaubt"}, status=400)
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    content = request.POST.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "Kommentar darf nicht leer sein"}, status=400)
    author = request.GET.get("username")
    comment = Comment.objects.create(post=post, author=author, content=content)
    return JsonResponse({
        "author": author,
        "content": comment.content,
        "created_at": comment.created_at.strftime("%d.%m.%Y %H:%M")
    })
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
    username = request.GET.get("username", "")
    password = request.GET.get("password", "")
    query    = request.GET.get("q", "").strip()
    users    = []

    if query:
        try:
            with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
                all_users = json.load(f)
            for u in all_users:
                uname = u.get('username') or ''
                if query.lower() in uname.lower():
                    users.append(u)
        except FileNotFoundError:
            print(f"users.json nicht gefunden unter {USER_JSON_PATH}")
        except json.JSONDecodeError:
            print("users.json enthält ungültiges JSON")

    return render(request, "meine_app/suche.html", {
        'username': username,
        'password': password,
        'users':    users,
        'query':    query,
    })

@check_login
def profilseite(request):
    # Wer ruft auf und wer wird angezeigt?
    current_user = request.GET.get("username", "")
    password     = request.GET.get("password", "")
    profile_user = request.GET.get("profil", current_user)

    # Beiträge des Profil-Users laden
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')

    # Profil-Daten aus users.json holen
    try:
        with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
            all_users = json.load(f)
        user_data = next((u for u in all_users if u.get('username') == profile_user), {})
    except Exception:
        user_data = {}

    avatar_url = user_data.get('avatar_url', '')
    bio        = user_data.get('bio', '')
    location   = user_data.get('location', '')

    return render(request, "meine_app/profilseite.html", {
        'username':     current_user,
        'password':     password,
        'profile_user': profile_user,
        'posts':        posts,
        'avatar_url':   avatar_url,
        'bio':          bio,
        'location':     location,
    })

@check_login
def edit_profile(request):
    username = request.GET.get("username", "")
    password = request.GET.get("password", "")

    # JSON laden und aktuellen Nutzer finden
    with open(USER_JSON_PATH, 'r', encoding='utf-8') as f:
        all_users = json.load(f)
    user_data = next((u for u in all_users if u.get('username') == username), None)
    if user_data is None:
        return redirect(f"{reverse('startseite')}?username={username}&password={password}")

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            avatar_file = form.cleaned_data['avatar']
            if avatar_file:
                fs = FileSystemStorage(
                    location=os.path.join(settings.MEDIA_ROOT, 'profile_pics'),
                    base_url=settings.MEDIA_URL + 'profile_pics/'
                )
                fname = f"{username}_{avatar_file.name}"
                saved_name = fs.save(fname, avatar_file)
                user_data['avatar_url'] = fs.url(saved_name)
            user_data['bio']      = form.cleaned_data['bio']
            user_data['location'] = form.cleaned_data['location']

            with open(USER_JSON_PATH, 'w', encoding='utf-8') as f:
                json.dump(all_users, f, indent=2, ensure_ascii=False)

            return redirect(
                f"{reverse('profilseite')}?username={username}"
                f"&password={password}&profil={username}"
            )
    else:
        form = ProfileForm(initial={
            'bio':      user_data.get('bio', ''),
            'location': user_data.get('location', '')
        })

    return render(request, "meine_app/edit_profile.html", {
        'form':       form,
        'avatar_url': user_data.get('avatar_url', ''),
        'username':   username,
        'password':   password,
    })

#   username = request.GET.get("us
@check_login
def einstellungen(request):
    username = request.GET.get("username")
    password = request.GET.get("password")
    return render(request, "meine_app/einstellungen.html", {"username": username, "password": password})
