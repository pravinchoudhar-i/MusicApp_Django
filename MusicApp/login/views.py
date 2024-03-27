from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.core.exceptions import ValidationError
from .validate import *
from django.core.exceptions import ValidationError
# from crud_app.models import *

# Create your views here.

class UserLogin(View):
    def get(self,request, *args, **kwargs):
        return render(request,'login.html')
    def post(self,request, *args, **kwargs):
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            user_details = UserDetails.objects.filter(user=user).first()
            request.session['role'] = user_details.role.name
            login(request,user)
            return redirect('project-management')       
        else:
            return render(request,'login.html')

class UserSignup(View):
    def get(self,request, *args, **kwargs):
        return render(request,'signup.html')

    def post(self,request, *args, **kwargs):
        validators = [UserAttributeSimilarityValidator,MinimumLengthValidator, NumericPasswordValidator]
        
        filled_data = dict(request.POST)
        filled_data.pop('csrfmiddlewaretoken')
        
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password1', None)
        conform_pwd = request.POST.get('password2', None)

        if password != conform_pwd:
            context = {
                "filled_data":filled_data
            }
            messages.error(request, ('Password and Confirm Password does not match'))
            return render(request, 'signup.html', context)
        else:
            try:
                for validator in validators:
                    if validator == UserAttributeSimilarityValidator:
                        user_attributes_array = (username, email)
                        er = validator().validate(password, user_attributes_array)
                    else:
                        er = validator().validate(password)
            except ValidationError as e:
                messages.error(request, str(e.message))
                context = {
                	"filled_data":filled_data
            	}
                return render(request, 'signup.html', context)

            hashed_pwd = make_password(password)

            check_email = User.objects.filter(email=email).exists()
            if check_email:
                messages.error(request, ("User with this email already exist's, please try again with new one."))
                context = {
                    "filled_data":filled_data
                    }
                return render(request, 'signup.html',context)
            else:
                try:
                    user = User(username=username,email=email,password=hashed_pwd)
                    user.save()
                    # setting default role for user 
                    role = Roles.objects.get(name="customer")
                    user_detail = UserDetails(user_id=user.id, role_id=role.id)
                    user_detail.save()
                    if user:
                        messages.success(request, ("Account Created Successfully"))
                        return redirect('user-login')
                except Exception as ex:
                    messages.error(request, ("User with this username already exist's, please try again with new one."))
                    context = {
                        "filled_data":filled_data
                    }
                    return render(request, 'signup.html',context)

        

