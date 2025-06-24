import json
import os
from django.conf import settings
from django.shortcuts import redirect

USER_JSON_PATH = os.path.join(settings.BASE_DIR, 'meine_app', 'backend', 'registrierung_login', 'users.json')

def check_login(view_func):
    def wrapper(request, *args, **kwargs):
        username = request.GET.get("username")
        password = request.GET.get("password")

        if not username or not password:
            return redirect("/login")

        try:
            with open(USER_JSON_PATH, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for user_data in users:
            if user_data['username'] == username and user_data['password'] == password:
                request.user = type("User", (), {"username": username})()  # Dummy-User setzen
                return view_func(request, *args, **kwargs)

        return redirect("/login")

    return wrapper
