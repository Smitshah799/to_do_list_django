from django.db import models
from django.contrib.auth.models import User as DjangoUser

class Note(models.Model):
    data = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, related_name='notes')

class NoteUsers(models.Model):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=150, null=True)
    password = models.CharField(max_length=150, null=True)
    
