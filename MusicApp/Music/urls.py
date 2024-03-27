from django.urls import path
from Music import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.AddSongView.as_view(), name='addsong'),
    path('liked-song/',views.LikedSongView.as_view() , name='likedsong'),
    path('playlist/', views.CreatePlaylistView.as_view(), name='playlist'),
    # path('show-playlist/', views.ShowPlaylistView.as_view(), name='showplaylist'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)