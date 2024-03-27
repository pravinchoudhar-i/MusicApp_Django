from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('',UserLogin.as_view(), name='user-login'),
    path('signup',UserSignup.as_view(), name='user-signup'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='user-logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html'
        ),
        name='password_reset'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='password_reset_done.html'
         ),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),
    # path('oauth/', include('social_django.urls', namespace='social')),
    

]