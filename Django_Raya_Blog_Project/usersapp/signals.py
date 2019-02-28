from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) # creates a user profile object with user instance

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() # saves the created user profile object whenever a user is created
