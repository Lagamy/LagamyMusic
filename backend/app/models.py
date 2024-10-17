from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import FileExtensionValidator

class Author(AbstractUser):
    image = models.ImageField(upload_to='Images/Users/', blank=True, null=True)

class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Album(models.Model):
    image = models.ImageField(upload_to='Images/Albums/', blank=True, null=True)
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='albums', blank=True, null=True, on_delete=models.CASCADE)

class Music(models.Model):
    image = models.ImageField(upload_to='Images/Music/', blank=True, null=True)
    audiotrack = models.FileField(upload_to='AudioTracks/', blank=True, validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])])
    name = models.CharField(max_length=200)
    author = models.ForeignKey(Author, related_name='singles', blank=True, null=True, on_delete=models.CASCADE) # For Singles, albums model covers author otherwise
    album = models.ForeignKey(Album, related_name='musics', blank=True, null=True, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, related_name='musics', blank=True, null=True, on_delete=models.SET_NULL)
    views = models.IntegerField(default=0)
# Create your models here.

