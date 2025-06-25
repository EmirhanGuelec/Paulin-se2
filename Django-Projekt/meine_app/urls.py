# meine_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                       views.startseite,           name='startseite'),
    path('post/create/',           views.create_post,         name='create_post'),
    path('post/toggle-like-ajax/', views.toggle_like_ajax,    name='toggle_like_ajax'),
    path('post/add-comment-ajax/', views.add_comment_ajax,    name='add_comment_ajax'),
    path('post/<int:post_id>/comment/', views.add_comment,    name='add_comment'),

    path('suche/',                 views.suche,               name='suche'),

    # hier ggf. weitere Routen: profilseite, freunde, impressum, etc.
    path('chat/',                  views.chat,                name='chat'),
    path('freunde/',               views.freunde,             name='freunde'),
    path('impressum/',             views.impressum,           name='impressum'),
    path('login/',                 views.login,               name='login'),
    path('login_check/',           views.login_check,         name='login_check'),
    path('posten/',                views.posten,              name='posten'),
    path('registrierung/',         views.registrierung,       name='registrierung'),
    path('suche/',                 views.suche,               name='suche'),
    path('einstellungen/',         views.einstellungen,       name='einstellungen'),
    path('profilseite/',           views.profilseite,         name='profilseite'),
    path('profil/edit/',           views.edit_profile,        name='edit_profile'),
]
