from django.db import models
from django.contrib.auth.models import User


# class NoteUser(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, null=True)
#     email = models.EmailField(max_length=200, null=True)
#     date_created = models.DateField(auto_now_add=True, null=True)
#     login_attempts = models.IntegerField(default=0)
#     last_login_attempt = models.DateTimeField(null=True, blank=True)
#     blocked_until = models.DateTimeField(null=True, blank=True)  # Add this line

#     def __str__(self):
#         return f"{self.user.username}" if self.name else f"{self.user.username}"
class NoteUser(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    blocked_ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}" if self.name else f"{self.user.username}"

class Note(models.Model):
    data = models.TextField(max_length=1000000)
    date = models.DateField(auto_now_add=True, null=True)
    user = models.ForeignKey(NoteUser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user} : {self.data}"
