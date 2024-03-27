from django.contrib import admin
from .models import AddSong,CreatePlaylist


# Register your models here.
@admin.register(AddSong)    
class AddSongAdmin(admin.ModelAdmin):
    list_display = ["song_name","artist","genre","release_year","song_file","add_to_like"]

admin.site.register(CreatePlaylist)