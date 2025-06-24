import json
from django.shortcuts import render, redirect
from django.contrib import messages

def login_check(request, user_json_path):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')

        if not username or not password:
            return render(request, 'meine_app/login.html', {"fehler": True})

        try:
            with open(user_json_path, 'r') as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = []

        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect(f"/startseite/?username={username}&password={password}")

        return render(request, 'meine_app/login.html', {"fehler": True})

    return render(request, 'meine_app/login.html')
