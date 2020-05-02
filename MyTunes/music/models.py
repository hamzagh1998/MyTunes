from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
import os

def albumImageUploadLocation(instance, filename):
    file_path = f"user/album/{instance.user.id}/{instance.user.username}-{filename}"
    return file_path

def songUploadLocation(instance, filename):
    file_path = f"user/song/{instance.album.user.id}/{instance.album.user.username}-{filename}"
    return file_path

CHOICES = (('public', 'public'), ('private', 'private'))

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=100, blank=False)
    genre = models.CharField(max_length=50, blank=True, help_text="optional")
    image = models.ImageField(default="logo.png", upload_to=albumImageUploadLocation)
    discription = models.TextField(help_text="optional", blank=True)
    is_favorite = models.BooleanField(default=False)
    is_public = models.CharField(max_length=50, blank=True, default="Public", choices=CHOICES, verbose_name="who can see this album")
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def summary(self):
        return self.discription[:50]+'...'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username+"-"+self.title)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=False)
    song_file = models.FileField(blank=False, upload_to=songUploadLocation)
    is_favorite = models.BooleanField(default=False)
    inserted_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.album.title+'-'+self.title+'-'+self.album.user.username


@receiver(post_delete, sender=Album)
def delete_image(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Album` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=Album)
def auto_delete_image_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Album` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Album.objects.get(pk=instance.pk).image
    except Album.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(post_delete, sender=Song)
def delete_file(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Song` object is deleted.
    """
    if instance.song_file:
        if os.path.isfile(instance.song_file.path):
            os.remove(instance.song_file.path)

@receiver(pre_save, sender=Song)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Song` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Song.objects.get(pk=instance.pk).song_file
    except Song.DoesNotExist:
        return False

    new_file = instance.song_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
