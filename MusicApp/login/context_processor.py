from crud_app.models import Roles, UserDetails

def privileges(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        # print(request.session['role'])
        # When user login through social media 
        user_detail = UserDetails.objects.filter(user_id=request.user.id).exists()
        if not user_detail:
            # setting default role for user
            role = Roles.objects.get(name="customer")
            user_details = UserDetails(user_id=request.user.id, role_id=role.id)
            user_details.save()
            request.session['role'] = user_details.role.name
        else:
            user_details = UserDetails.objects.filter(user=request.user).first()
            request.session['role'] = user_details.role.name
            
        if request.session['role']:
            privileges = Roles.objects.filter(name=request.session['role']).values_list('privileges__name',flat=True)
            user_profile = UserDetails.objects.get(user_id=request.user.id)
        else:
            privileges = []
            user_profile = []
        print(privileges)
        
    else:
        privileges = []
        user_profile = []
        
    return {
        'privileges' : privileges,
        'user_profile' : user_profile
    }

