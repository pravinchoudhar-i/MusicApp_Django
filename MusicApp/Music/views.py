'''
Date of creation: 18:19:14 07-01-2024
Created by: USER NAME 
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import *
from datetime import datetime
from django.contrib import messages
import json
from django.db.models import Q
import os
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError

class AddSongView(View):

    def __init__(self,*args,**kwargs):
        path = os.getcwd()

        with open(os.path.join(path, "form_jsons/AddSong.json"), 'r') as file:
            self.queryset = file.read()

    def get(self,request,*args, **kwargs):
        file = self.queryset 
        queryset_dict = json.loads(file)

        action = request.GET.get('action',None)
        instance_id = request.GET.get('id',None)
        search = request.GET.get('search',None)
        entries = request.GET.get('entries', '4')

        table_values = queryset_dict['HTML_table']['values']
        list_table_values = [x["name"] for x in table_values]
        
        if action == 'create':	
            context = {
                "redirect":"addsong"
            }       
            return render(request, 'create.html', context)

        elif action == 'edit':
            if instance_id:
                data = AddSong.objects.filter(status_code=1).get(id=instance_id)

                

                json_string = str(queryset_dict)
                context = {"data":data, "redirect":"addsong", }
                return render(request,'edit.html',context,)

        elif action == 'delete':	
            if instance_id:
                return self.delete(request)

        elif action == 'search':
            data = AddSong.objects.filter(Q(song_name__icontains=search)|Q(artist__icontains=search)|Q(genre__icontains=search)|Q(song_file__icontains=search)|Q(add_to_like__icontains=search),status_code=1).all()

            paginator = Paginator(data, int(entries)) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            pagination_url = request.path + "?entries=" + entries + "&search=" + search + "&action=" + action + "&"

            #TODO: Uncomment if checkbox field is included in the form.
            # for i in data:
            # 	var =i.checkbox.replace("[","")
            # 	var = var.replace("]","")
            # 	var = var.replace("'", "")
            # 	var = var.split(",")
            # 	i.checkbox = var
            # 	i.save()

            context = {
                "data":data, 
                "values":table_values, 
                "JsonForm": queryset_dict, 
                "redirect":"addsong",
                "entries" : entries,
                "page_obj" : page_obj,  
                "pagination_url" : pagination_url,
                }
            return render(request,'table.html',context)

        else:    						
            data = AddSong.objects.filter(status_code = 1).only(*list_table_values)


            paginator = Paginator(data, int(entries)) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            if action:
                pagination_url = request.path + "?entries=" + entries + "&action=" + action + "&"          
            else:
                pagination_url = request.path + "?entries=" + entries + "&"


            #TODO: Uncomment if checkbox field is included in the form.
            
            #for i in data:
                #var =i.checkbox.replace("[","")
                #var = var.replace("]","")
                #var = var.replace("'", "")
                #var = var.split(",")
                #i.checkbox = var
                #i.save()

            context = {
                "data":data,
                "redirect":"addsong",
                "values":table_values,
                "JsonForm": queryset_dict,
                "entries" : entries,
                "page_obj" : page_obj,
                   "pagination_url" : pagination_url
            }
            return render(request,'table.html',context)

    # Create
    def post(self,request,*args, **kwargs):
        if '_put' in request.POST:
            return self.put(request)
              
        
        song_name = request.POST.get('song_name', None)
        artist = request.POST.get('artist', None)
        genre = request.POST.get('genre', None)
        release_year = request.POST.get('release_year', None)
        song_file = request.FILES.get('song_file',None)
        add_to_like = request.POST.get('add_to_like',None) 

        
        
        
        data = AddSong.objects.create(song_name = song_name, artist = artist, genre = genre, release_year = release_year, song_file = song_file, add_to_like = add_to_like)

        if data:
            return redirect('addsong')

    # Edit
    def put(self,request,*args,**kwargs):
        
        song_name = request.POST.get('song_name', None)
        artist = request.POST.get('artist', None)
        genre = request.POST.get('genre', None)
        release_year = request.POST.get('release_year', None)
        song_file = request.FILES.get('song_file',None)
        add_to_like = request.POST.get('add_to_like',None) 
        
        id   = request.POST.get('id',None)
  
        update = AddSong.objects.filter(id=id).update(
        song_name=song_name,
        artist=artist,
        genre=genre,
        release_year=release_year,
        song_file=song_file,
        add_to_like=add_to_like
    )

    # else:
    #     old_data = AddSong.objects.get(id=id)
    #     update = AddSong.objects.filter(id=id).update(
    #         song_name=song_name,
    #         artist=artist,
    #         genre=genre,
    #         release_year=release_year,
    #         song_file=song_file,
    #         add_to_like=add_to_like
    #     )
        # if add_to_like not in ['True', 'False', None]:
        #      raise ValidationError("Invalid value for add_to_like")
         
        # add_to_like = add_to_like == 'True' if add_to_like is not None else None

        if update:
            return redirect('addsong')
        else:
            return HttpResponse("Not updated")
  
    # Delete
    def delete(self,request,*args,**kwargs):
        id = request.GET.get('id',None)

        update = AddSong.objects.filter(id=id).update(status_code=0)
        if update:
            return redirect('addsong')
        else:
            return HttpResponse("Not updated")


        #TODO: Implement IF validation if file field available in the form

        #if file:
            #obj = AddSong.objects.get(id=id)
            #'''obj.song_file= song_file
''' 
            #obj.save()
   
        # TODO: Remove file field
        update = AddSong.objects.filter(id=id).update(song_name = song_name, artist = artist, genre = genre, release_year = release_year, song_file = song_file, add_to_like = add_to_like)
        
        #else: 
        #	old_data = AddSong.objects.get(id=id)

        #	update = AddSong.objects.filter(id=id).update(song_name = song_name, artist = artist, genre = genre, release_year = release_year, song_file = song_file, add_to_like = add_to_like)

        if update:
            return redirect('addsong')
        else:
            return HttpResponse("Not updated")
'''
    

class LikedSongView(View):
    
    def get(self, request, *args, **kwargs):
    
        liked_song=AddSong.objects.filter(add_to_like=True)
  
        context ={
            'liked_song':liked_song
        }
        return render(request,'liked.html',context)
    
    def delete(self,request,*args,**kwargs):
        id = request.GET.get('id',None)

        update = AddSong.objects.filter(id=id).update(status_code=0)
        if update:
            return redirect('likedsong')
        else:
            return HttpResponse("Not updated")


# class LikedSongsView(View):
#     template_name = 'liked_songs.html'

#     def get(self, request, *args, **kwargs):

#         liked_songs = SongDetails.objects.filter(add_to_favorite=True)

#         context = {'liked_songs': liked_songs}
#         return render(request, self.template_name, context)



class CreatePlaylistView(View):

    def __init__(self,*args,**kwargs):
        path = os.getcwd()

        with open(os.path.join(path, "form_jsons/Playlist.json"), 'r') as file:
            self.queryset = file.read()

    def get(self,request,*args, **kwargs):
        file = self.queryset 
        queryset_dict = json.loads(file)

        action = request.GET.get('action',None)
        instance_id = request.GET.get('id',None)
        search = request.GET.get('search',None)
        entries = request.GET.get('entries', '5')

        table_values = queryset_dict['HTML_table']['values']
        list_table_values = [x["name"] for x in table_values]
        
        # show_song=AddSong.objects.values('song_name').all()
        show_song=AddSong.objects.filter(status_code = 1)
  
        if action == 'create':	
            
            
            context = {
                "redirect":"playlist",
                'show_song':show_song
            }       
            return render(request, 'C_Playlist.html', context)

        elif action == 'edit':
            if instance_id:
                data = CreatePlaylist.objects.filter(status_code=1).get(id=instance_id)

                

                json_string = str(queryset_dict)
                context = {"data":data, "redirect":"playlist", }
                return render(request,'edit.html',context)

        elif action == 'delete':	
            if instance_id:
                return self.delete(request)

        elif action == 'search':
            data = CreatePlaylist.objects.filter(Q(playlist_name__icontains=search)|Q(song_name__icontains=search),status_code=1).all()

            paginator = Paginator(data, int(entries)) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            pagination_url = request.path + "?entries=" + entries + "&search=" + search + "&action=" + action + "&"

            #TODO: Uncomment if checkbox field is included in the form.
            #for i in data:
                #var =i.checkbox.replace("[","")
                #var = var.replace("]","")
                #var = var.replace("'", "")
                #var = var.split(",")
                #i.checkbox = var
                #i.save()

            context = {
                "data":data, 
                "values":table_values, 
                "JsonForm": queryset_dict, 
                "redirect":"playlist",
                "entries" : entries,
                "page_obj" : page_obj,
                "pagination_url" : pagination_url,
                }
            return render(request,'C_Playlist.html',context)

        else:    						
            data = CreatePlaylist.objects.filter(status_code = 1).only(*list_table_values)


            paginator = Paginator(data, int(entries)) 
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            if action:
                pagination_url = request.path + "?entries=" + entries + "&action=" + action + "&"          
            else:
                pagination_url = request.path + "?entries=" + entries + "&"


            #TODO: Uncomment if checkbox field is included in the form.
            
            #for i in data:
                #var =i.checkbox.replace("[","")
                #var = var.replace("]","")
                #var = var.replace("'", "")
                #var = var.split(",")
                #i.checkbox = var
                #i.save()

            context = {
                "data":data,
                "redirect":"playlist",
                "values":table_values,
                "JsonForm": queryset_dict,
                "entries" : entries,
                "page_obj" : page_obj,
                "pagination_url" : pagination_url
            }
            return render(request,'C_Playlist.html',context)

    # Create
    def post(self,request,*args, **kwargs):
        if '_put' in request.POST:
            return self.put(request)
            
        
        playlist_name = request.POST.get('playlist_name', None)
        song_name = request.POST.get('song_name', None)
  
        try:
            song_instance = AddSong.objects.filter(song_name=song_name)
        except AddSong.DoesNotExist:
            return HttpResponse("Selected song not found.")
        
        
        # song_instance = AddSong.objects.get(id=id)
        
        data = CreatePlaylist.objects.create(playlist_name = playlist_name, song_name = song_instance)

        if data:
            return redirect('playlist')

    # Edit
    def put(self,request,*args,**kwargs):
        
        playlist_name = request.POST.get('playlist_name', None)
        song_name = request.POST.get('song_name', None)
        
        id   = request.POST.get('id',None)

        #TODO: Implement IF validation if file field available in the form

        #if file:
            #obj = CreatePlaylist.objects.get(id=id)
            #''''''
            #obj.save()
        # TODO: Remove file field
        update = CreatePlaylist.objects.filter(id=id).update(playlist_name = playlist_name, song_name = song_name)
        
        #else: 
        #	old_data = CreatePlaylist.objects.get(id=id)

        #	update = CreatePlaylist.objects.filter(id=id).update(playlist_name = playlist_name, song_name = song_name)

        if update:
            return redirect('playlist')
        else:
            return HttpResponse("Not updated")

    # Delete
    def delete(self,request,*args,**kwargs):
        id = request.GET.get('id',None)

        update = CreatePlaylist.objects.filter(id=id).update(status_code=0)
        if update:
            return redirect('playlist')
        else:
            return HttpResponse("Not updated")
        
# class ShowPlaylistView(View):
#     def get(self, request, *args, **kwargs):
        
        
#         playlist_instance=CreatePlaylist.objects.all()
        
#         context={
            
#             "playlist_instance":playlist_instance,
#         }
        
      
#         return render(request,'show_playlist1.html',context)
    