from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Music, Album, Author, Genre


class AuthorForm(UserCreationForm):
    image = forms.ImageField(label='Image', required=False)

    def clean(self):
        image = self.cleaned_data.get('image', None)
        if not image:
            raise ValidationError({'image': "No image was selected."})

    class Meta:
        model = Author
        fields = ('username', 'email', 'password1', 'password2', 'image')


class AlbumForm(forms.ModelForm):
    def clean(self):
        image = self.cleaned_data.get('image', None)
        name = self.cleaned_data.get('name', None)
        if not name:
            raise ValidationError({'name': "Album name is empty."})
        if not image:
            raise ValidationError({'image': "No image was selected."})
    class Meta:
        model = Album
        fields = ['image', 'name']

class MusicForm(forms.ModelForm):
    def clean(self):
        name = self.cleaned_data.get('name', None)
        image = self.cleaned_data.get('image', None)
        audiotrack = self.cleaned_data.get('audiotrack', None)
        genre = self.cleaned_data.get('genre', None)
        if not name:
            raise ValidationError({'name': "Music name is empty."})
        if not audiotrack:
            raise ValidationError({'audiotrack': "No audio was selected."})
        if not image:
            raise ValidationError({'image': "No image was selected."})
        if not genre:
            raise ValidationError({'genre': "No genre was selected."})

    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True, empty_label="Select Genre")
    class Meta:
        model = Music
        fields = ['image', 'name', 'audiotrack', 'genre']


# class MusicGenreForm(forms.Form):
#     genre = forms.ModelChoiceField(queryset=Genre.objects.all(), required=True, empty_label="Select Genre")

class GenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name']
