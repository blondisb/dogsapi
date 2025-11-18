from django.db import models

class Breed(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'breeds'

class Dog(models.Model):
    name = models.CharField(max_length=200)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='dogs')
    
    class Meta:
        db_table = 'dogs'