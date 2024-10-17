from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from app.models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Confirm password field
    image = serializers.ImageField(write_only=True, required=True)

    class Meta:
        model = Author
        fields = ['username', 'image', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = Author.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            image='image'
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError("Username and password are required.")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid username or password.")

        return {
            'user': user
        }



class AddMediaSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True, required=True)
    image = serializers.CharField(write_only=True, required=True)
    audiotrack = serializers.CharField(write_only=True, required=True)
    isAlbum = serializers.BooleanField(write_only=True, required=True)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), write_only=True, required=True)
    def create(self, validated_data):
        if validated_data['isAlbum']:
            media = Album.objects.create(
                name=validated_data['name'],
                image=validated_data['image'],
                author=validated_data['author']
            )
            message = 'Added Album!'
        else:
            media = Music.objects.create(
                name=validated_data['name'],
                image=validated_data['image'],
                audiotrack=validated_data['audiotrack'],
                author=validated_data['author']
            )
            message = 'Added Single!'
        media.save()
        return media, message

class AddSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['name', 'image', 'audiotrack', 'author']
    def create(self, validated_data):
        # no need to manually map fields, validated_data already matches model fields
        return Music.objects.create(**validated_data)

class AddMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['name', 'image', 'audiotrack', 'album']
    def create(self, validated_data):
        return Music.objects.create(**validated_data)


class AddAlbumSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=True)
    image = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = Music
        fields = ['name', 'image', 'author']
    def create(self, validated_data):
        # manual mapping
        single = Album.objects.create(
            name=validated_data['name'],
            image=validated_data['image'],
            author=validated_data['author']
        )
        single.save()
        return single


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = ['id', 'name', 'image', 'audiotrack']


class AlbumSerializer(serializers.ModelSerializer):
    music = MusicSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Album
        fields = ['id', 'name', 'image', 'author', 'music']


class AuthorSerializer(serializers.ModelSerializer):
    # Without this 'albums' and 'singles' fields would return just ids
    albums = AlbumSerializer(many=True, read_only=True, required=False)  # automatically gets all albums related to that author as objects without views, using ForeignKeys
    singles = MusicSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Author
        fields = ['id', 'username', 'image', 'albums', 'singles']


    # Would use this if I need to display full author info other places besides viewAuthor:
    # def get_singles(self, obj):
    #     return MusicSerializer(Music.objects.filter(author=obj.id, album=None), many=True).data


class GenreSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True, required=False)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'musics']


# class GenreMapSerializer(serializers.Serializer):
#     genres = GenreSerializer(many=True, required=False)
#     # genre = GenreSerializer()
#     # music = MusicSerializer(many=True)
#     #
#     # def to_representation(self, instance):
#     #     # Custom logic to handle the map serialization
#     #     return {
#     #         'genre': GenreSerializer(instance['genre']).data,
#     #         'music': MusicSerializer(instance['music'], many=True).data
#     #     }
#
#
# class AuthorListSerializer(serializers.Serializer):
#     authors = AuthorSerializer(many=True, required=False)
