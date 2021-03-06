# Generated by Django 2.2.12 on 2020-05-02 07:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('genre', models.CharField(blank=True, help_text='optional', max_length=50)),
                ('image', models.ImageField(default='logo.png', upload_to=music.models.albumImageUploadLocation)),
                ('discription', models.TextField(help_text='optional')),
                ('is_favorite', models.BooleanField(default=False)),
                ('is_public', models.CharField(blank=True, choices=[('all', 'all'), ('just me', 'just me')], default='all', max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('song_file', models.FileField(upload_to=music.models.songUploadLocation)),
                ('is_favorite', models.BooleanField(default=False)),
                ('inserted_created', models.DateTimeField(auto_now_add=True)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='music.Album')),
            ],
        ),
    ]
