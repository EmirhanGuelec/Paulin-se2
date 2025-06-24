from django.urls import path
from . import views

urlpatterns = [
    # Startseite & Post-Funktionen
    path('', views.startseite, name='startseite'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),


    # Statische Seiten und Navigation
    path('chat/', views.chat, name='chat'),
    path('freunde/', views.freunde, name='freunde'),
    path('impressum/', views.impressum, name='impressum'),
    path('login/', views.login, name='login'),
    path('login_check/', views.login_check, name='login_check'),
    path('posten/', views.posten, name='posten'),
    path('registrierung/', views.register, name='registrierung'),
    path('suche/', views.suche, name='suche'),
    path('einstellungen/', views.einstellungen, name='einstellungen'),
]

