from rest_framework import serializers
from .models import Breed, Dog

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class DogSerializer(serializers.ModelSerializer):
    breed = serializers.StringRelatedField()
    breed__name = serializers.CharField(source='breed.name', read_only=True)
    
    class Meta:
        model = Dog
        fields = ['id', 'name', 'breed', 'breed__name']

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class AnswerSerializer(serializers.Serializer):
    totalBreeds = serializers.IntegerField()
    totalDogs = serializers.IntegerField()
    commonBreed = serializers.CharField(max_length=200)
    commonDogName = serializers.CharField(max_length=200)