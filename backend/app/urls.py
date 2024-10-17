from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

from project import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path('register', views.register, name='register'),
    # path('login', auth_views.LoginView.as_view(template_name='loginUser.html'), name='login'),
    # path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path("authors", views.ShowAuthors.as_view(), name="Authors"),
    path("add-genre", views.addGenre, name="addGenre"),
    path("genres", views.ShowGenres.as_view(), name="Genres"),
    path("<author_id>/add-album-or-single", views.addAlbumOrSingle, name="addAlbumOrSingle"),
    path("<author_id>/add-single", views.addSingle, name="addSingle"),
    path("<author_id>/add-album", views.addAlbum, name="addAlbum"),
    path("<author_id>/album/<album_id>/add-music", views.addMusic, name="addMusic"),
    path("<author_id>", views.ViewAuthor.as_view(), name="Author"),
    path("<author_id>/album/<album_id>/", views.ViewAlbum.as_view(), name="Album"),
    path("<author_id>/single/<music_id>/", views.ViewSingle.as_view(), name="Single"),
    path('<music_id>/remove-music/', views.removeMusic, name='removeMusic'),
    path('<album_id>/remove-album/', views.removeAlbum, name='removeAlbum'),
    path('remove-album/<album_id>/', views.removeAlbum, name='removeAlbum'),
]
