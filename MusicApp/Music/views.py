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
		entries = request.GET.get('entries', '10')

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
				return render(request,'edit.html',context)

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
			for i in data:
				var =i.checkbox.replace("[","")
				var = var.replace("]","")
				var = var.replace("'", "")
				var = var.split(",")
				i.checkbox = var
				i.save()

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
		add_to_like = request.POST.get('add_to_like', False) 
		
		
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
		add_to_like = request.POST.getlist('add_to_like', None)
		
		id   = request.POST.get('id',None)
  
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
    

