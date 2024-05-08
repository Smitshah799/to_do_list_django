from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import NoteUser

@receiver(post_save, sender=User)
def add_superuser_to_admin_group(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        admin_group, created = Group.objects.get_or_create(name='admin')
        instance.groups.add(admin_group)

@receiver(post_save, sender=User)
def add_user_to_groups(sender, instance, created, **kwargs):
    if created:
        noteuser_group, created = Group.objects.get_or_create(name='noteuser')

        instance.groups.add(noteuser_group)

        NoteUser.objects.create(user=instance, name=instance.username, email=instance.email)