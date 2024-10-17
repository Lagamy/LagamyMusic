import jwt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from app.middleware import encode_jwt, decode_jwt, getCurrentUser, revalidateToken, CanEdit
from app.serializers import *
from app.forms import *
from app.models import *
from django.urls import reverse
import os

from project import settings


def home(request):
    # print(slugify("Bring me the horizon"))
    return render(request, "index.html")


@csrf_exempt
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if not serializer.is_valid(): # calls validate() method in the serializer and if false - rises 400
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()  # calls create() method in the serializer

    # creating JWT after successful registration
    user = Author.objects.get(username=serializer.data.get('username'))
    token = encode_jwt({'user_id': user.id})

    # returns response with JWT
    response = Response({'message': 'Registration successful!'})
    response.set_cookie('jwt', token, httponly=True, secure=True)  # set JWT in HttpOnly cookie
    return response
@csrf_exempt
@api_view(['POST'])
def logout(request):
    response = Response({'message': 'Logout successful!'})
    response.set_cookie('jwt', path='/', httponly=True, secure=True, samesite='None', expires=timezone.now())
    return response
@csrf_exempt
@api_view(['POST'])
def login(request):
    print("Request Data:", request.data)  # Debug print to verify incoming request data
    serializer = LoginSerializer(data=request.data)

    if not serializer.is_valid(): # calls validate() method in the serializer and if false - rises 400
        print("Serializer errors:", serializer.errors)  # Print validation errors
        error_message = serializer.errors.get('non_field_errors', [])[0] # gets first error
        return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)

    # creating JWT after successful registration
    user = serializer.validated_data.get('user')
    token = encode_jwt({'user_id': user.id})
    print("Generated Token:", token)
    # returns response with JWT
    response = Response({'message': 'Login successful!'})
    # expires = timezone.now() + settings.JWT_EXPIRATION_DELTA
    response.set_cookie('jwt', token, httponly=True, secure=True, samesite='None')  # set JWT in HttpOnly cookie

    return response

class ViewUser(APIView):
    def get(self, request):
        user_id, token = getCurrentUser(request)

        if user_id is not None:
            user = get_object_or_404(Author, id=user_id)
            serializer = AuthorSerializer(user)
            data = serializer.data
            response = Response(data)
            if token is not None:
                # expires = timezone.now() + settings.JWT_EXPIRATION_DELTA
                response.set_cookie('jwt', token, httponly=True, secure=True, samesite='None')
            return response
        return Response({'error': 'No token'}, status=status.HTTP_401_UNAUTHORIZED)

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

@api_view(['POST'])
def addAlbumOrSingle(request, author_id):
    if CanEdit(request, author_id):
        serializer = AddMediaSerializer(data=request.data)
        media, message = serializer.save()  # saves serializer and returns media and message
        return Response({'message': message})
    else:
        return Response({'message': 'Forbidden'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def addSingle(request, author_id):
    if CanEdit(request, author_id):
        serializer = AddSingleSerializer(data=request.data)
        serializer.save()
        return JsonResponse({'message': 'Added Single!'})
    else:
        return Response({'message': 'Forbidden'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def addAlbum(request, author_id):
    if CanEdit(request, author_id):
        serializer = AddAlbumSerializer(data=request.data)
        serializer.save()
        return JsonResponse({'message': 'Added Album!'})
    else:
        return Response({'message': 'Forbidden'}, status=status.HTTP_400_BAD_REQUEST)


def addMusic(request, author_id):
    if CanEdit(request, author_id):
        serializer = AddMusicSerializer(data=request.data)
        media = serializer.save()
        return Response({'message': 'Added Music to ' + media.album.name + '!'})
    else:
        return Response({'message': 'Forbidden'}, status=status.HTTP_400_BAD_REQUEST)


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


class ShowAuthors(APIView):
    def get(self, request):
        authors = Author.objects.prefetch_related('albums', 'singles').all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)


class ShowGenres(APIView):
    def get(self, request):
        # moved empty(without music) genres filtering to React
        # genres = Genre.objects.annotate(music_count=Count('musics')).filter(music_count__gt=0).prefetch_related('musics')

        genres = Genre.objects.prefetch_related('musics') # makes dictionary without fetching each music in table seperately # Optimisation
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)


class ViewAuthor(APIView): # more complex than ViewAlbum and ViewSingle because of email
    # permission_classes = [IsAuthenticated]

    def get(self, request, author_id):
        author = get_object_or_404(Author.objects.prefetch_related('albums', 'singles'), id=author_id)
        can_edit, token = CanEdit(request, author_id)
        serializer = AuthorSerializer(author)
        data = serializer.data
        data['email'] = author.email if can_edit else ''  # So other users wouldn't be able to get each other email through frontend
        # I change database structure to make it so music that has author as foreign key is single. (Otherwise can still access author through music.album.author)
        # singles = Music.objects.filter(author=author.id, album=None)
        # data['singles'] = MusicSerializer(singles, many=True, required=False).data # Adding singles field to JSON. Can also be encapsulated in serializer if needed
        # update token if expired
        if token is not None:
            data.set_cookie('jwt', token, httponly=True, secure=True)
        return Response(data)
        # return render(request, "Author.html",{'author': author, 'albums': albums, 'singles': singles, 'can_edit': can_edit})


class ViewAlbum(APIView):
    def get(self, request, author_id, album_id):
        album = get_object_or_404(Album, id=album_id)
        serializer = AlbumSerializer(album)
        response = Response(serializer.data)
        revalidateToken(request, response)
        return response


class ViewSingle(APIView):
    def get(self, request, author_id, music_id):
        music = get_object_or_404(Music, id=music_id)
        serializer = MusicSerializer(music)
        response = Response(serializer.data)
        revalidateToken(request, response)
        return response


# Create your views here.



