from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Creates and links a profile instance when a user is created.
    # Updates profile when a user is saved.
    if created:
        Profile.objects.create(user=instance)
    if not Profile.objects.filter(user=instance):
        Profile.objects.create(user=instance)
    instance.profile.save()
