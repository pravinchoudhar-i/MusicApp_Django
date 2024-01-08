from django.urls import path
from Music import views



urlpatterns = [
    path('', views.AddSongView.as_view(), name='addsong'),

]