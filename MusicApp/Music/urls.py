from django.urls import path
from Music import views



urlpatterns = [
    path('', views.AddSongView.as_view(), name='addsong'),
    path('liked-song/',views.LikedSong , name='likedsong'),
    path('create-list/',views.CreatePlaylist , name='createplaylist'),

]