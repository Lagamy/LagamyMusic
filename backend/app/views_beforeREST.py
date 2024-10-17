from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from app.serializers import *
from app.forms import *
from app.models import *
from django.urls import reverse
import os


def home(request):
    # print(slugify("Bring me the horizon"))
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('{{user.id}}')
        else:
            # Print form errors to console
            print(form.errors)
    else:
        form = AuthorForm()
    return render(request, 'registerUser.html', {'form': form})


def addGenre(request):
    form = None
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES)
        if form.is_valid():
            # UseImageLink = request.POST.get('UseImageLink') #get checkbox from html
            # author = form.save(commit=False)
            # if UseImageLink == 'on':
            #     author.image = form.cleaned_data['image_link']
            #     # Использовать изображение, загруженное с устройства
            # else:
            #     author.image = form.cleaned_data['image']
            #     # Использовать ссылку на изображение
            genre = form.save(commit=False)
            genre.save()
            return redirect('Genres')
    else:
        form = GenreForm()
    return render(request, 'addGenre.html', {'form': form})


def addAlbumOrSingle(request):
    if request.user.is_authenticated:
        author = get_object_or_404(Author, id=request.user.id)
        single_form = MusicForm(request.POST, request.FILES)
        album_form = AlbumForm(request.POST, request.FILES)
        if request.method == 'POST':
            if 'single_submit' in request.POST:
                if single_form.is_valid():
                    music_item = single_form.save(commit=False)
                    music_item.author = author
                    music_item.save()
            else:
                if album_form.is_valid():
                    music_item = album_form.save(commit=False)
                    music_item.author = author
                    music_item.save()
            return redirect('Author', author.id)
        else:
            if 'single_submit' in request.POST:
                music_item = MusicForm()
            else:
                music_item = AlbumForm()
        return render(request, 'addAlbumOrSingle.html', {'single_form': single_form, 'album_form': album_form, 'author': author})
    else:
        return redirect("/")


# def addSingle(request):
#     if request.user.is_authenticated:
#         author = get_object_or_404(Author, id=request.user.id)
#         if request.method == 'POST':
#             form = MusicForm(request.POST, request.FILES)
#             if form.is_valid():
#                 music = form.save(commit=False)
#                 music.author = author
#                 music.save()
#                 user_url = reverse('Author', args=[author.id])
#                 return redirect(album_url)
#         else:
#             form = MusicForm()
#         return render(request, 'addMusic.html', {'form': form, 'author': author, 'is_single': True})
#     else:
#         return redirect("/")
# def addAlbum(request):
#     if request.user.is_authenticated:
#         author = get_object_or_404(Author, id=request.user.id)
#         if request.method == 'POST':
#             form = AlbumForm(request.POST, request.FILES)
#             if form.is_valid():
#                 album = form.save(commit=False)
#                 album.author = author
#                 album.save()
#                 album_url = reverse('Album', args=[request.user.id, album.id])
#                 return redirect(album_url)
#         else:
#             form = MusicForm()
#         return render(request, 'addAlbum.html', {'form': form, 'author': author})
#     else:
#         return redirect("/")


def addMusic(request, album_id):
    if request.user.is_authenticated:
        author = get_object_or_404(Author, id=request.user.id)
        album = get_object_or_404(Album, id=album_id)
        if album.author == author:
            if request.method == 'POST':
                form = MusicForm(request.POST, request.FILES)
                if form.is_valid():
                    music = form.save(commit=False)
                    music.album = album
                    music.author = author
                    music.save()
                    album_url = reverse('Album', args=[author.id, album.id])
                    return redirect(album_url)
            else:
                form = MusicForm()
            return render(request, 'addMusic.html', {'form': form, 'author': author, 'album': album, 'is_single': False})
    return redirect("/")


def removeAlbum(request, album_id):
    if request.user.is_authenticated:
        album = get_object_or_404(Album, id=album_id)
        if request.method == 'POST':
            associated_music = Music.objects.filter(album=album.id)
            for music in associated_music:
                os.remove(music.image.path)
                os.remove(music.audiotrack.path)
                music.delete()
            os.remove(album.image.path)
            album.delete()
            return redirect('Author', request.user.id)

def removeMusic(request, music_id):
    if request.user.is_authenticated:
        music = get_object_or_404(Music, id=music_id)
        if request.method == 'POST':
            os.remove(music.image.path)
            os.remove(music.audiotrack.path)
            music.delete()
            if music.album is not None:
                return redirect('Album', request.user.id, music.album.id)
            else:
                return redirect('Author', request.user.id)


def ShowAuthors(request):
    authors = Author.objects.all()
    return render(request, "ShowAuthors.html", {'authors': authors})


def ShowGenres(request):
    genres = Genre.objects.all()
    genre_music_map = {}
    for genre in genres:
        music = Music.objects.filter(genre=genre.id)
        genre_music_map[genre] = music
    return render(request, "ShowGenres.html", {'genre_music_map': genre_music_map})

def ViewAuthor(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    albums = Album.objects.filter(author=author.id)
    singles = Music.objects.filter(author=author.id, album=None)
    can_edit = request.user.is_authenticated and author.id == request.user.id
    return render(request, "Author.html", {'author': author, 'albums': albums, 'singles': singles, 'can_edit': can_edit})

def ViewAlbum(request, author_id, album_id):
    author = get_object_or_404(Author, id=author_id)
    album = get_object_or_404(Album, id=album_id)
    allmusic = Music.objects.filter(album=album_id)
    can_edit = request.user.is_authenticated and author.id == request.user.id
    return render(request, 'Album.html', {'author': author, 'album': album, 'allmusic': allmusic, 'can_edit': can_edit})


def ViewSingle(request, author_id, music_id):
    author = get_object_or_404(Author, id=author_id)
    music = get_object_or_404(Music, id=music_id)
    can_edit = request.user.is_authenticated and author.id == request.user.id
    return render(request, "Single.html", {'author': author, 'music': music, 'can_edit': can_edit})
# Create your views here.
