# Generated by Django 2.2.12 on 2020-05-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='discription',
            field=models.TextField(blank=True, help_text='optional'),
        ),
    ]