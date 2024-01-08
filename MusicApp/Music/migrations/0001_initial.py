# Generated by Django 5.0.1 on 2024-01-08 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_code', models.BooleanField(default=1)),
                ('song_name', models.CharField(blank=True, max_length=200, null=True)),
                ('artist', models.CharField(blank=True, max_length=200, null=True)),
                ('genre', models.CharField(blank=True, max_length=200, null=True)),
                ('release_year', models.IntegerField(blank=True, default=100, null=True)),
                ('song_file', models.FileField(blank=True, null=True, upload_to='Music_file')),
                ('add_to_like', models.BooleanField(blank=True, default=1, null=True)),
            ],
        ),
    ]