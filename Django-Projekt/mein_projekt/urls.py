from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from meine_app import views as app_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Authentifizierung und Registrierung
    path("login/", app_views.login, name='login'),
    path("login_check/", app_views.login_check, name='login_check'),
    path("registrierung/", app_views.register, name='register'),

    # Hauptfunktionen
    path("startseite/", app_views.startseite, name='startseite'),
    path("posten/", app_views.posten, name='posten'),
    path("upload/", app_views.saveUploadedFile),

    # Beiträge
    path("post/create/", app_views.create_post, name='create_post'),
    path("post/<int:post_id>/comment/", app_views.add_comment, name='add_comment'),
    path("post/<int:post_id>/like/", app_views.toggle_like, name='toggle_like'),

    # Seiten
    path("profilseite/", app_views.profilseite, name='profilseite'),
    path("chat/", app_views.chat, name='chat'),
    path("freunde/", app_views.freunde, name='freunde'),
    path("impressum/", app_views.impressum, name='impressum'),
    path("suche/", app_views.suche, name='suche'),
    path("einstellungen/", app_views.einstellungen, name='einstellungen'),

    # App-interne URLs (optional, falls du dort Routen definierst)
    path('', include('meine_app.urls')),
]

# Medien-Dateien im Entwicklungsmodus
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
