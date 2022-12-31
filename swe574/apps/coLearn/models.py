import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Username, first name, last name, password and e-mail adress
# is already handled by the django auth model. 
# The Profile Django model is used to store the extra information
# that relates to the built-in Django User model.
class CoLearnUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Used to extend the Auth User.
    interests = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    background = models.TextField(max_length=1000, blank=True)
    profile_picture = models.FileField(blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    birth_date = models.DateField(null=True, blank=True)


# Signal definition so that Profile model will be automatically
# created/updated when User instances are created/updated.
@receiver(post_save, sender=User)
def create_colearn_user(sender, instance, created, **kwargs):
    if created:
        CoLearnUser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_colearn_user(sender, instance, **kwargs):
    instance.colearnuser.save()

