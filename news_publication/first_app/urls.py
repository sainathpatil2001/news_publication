from django.urls import path,include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    #Admin Login releted urls paterns here 

    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup_view, name='signup'),  # Signup page
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Login page
    path('logout/', views.LogoutView.as_view(), name='logout'),  # Logout page
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='first_app/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='first_app/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='first_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='first_app/password_reset_complete.html'), name='password_reset_complete'),

    #writer login and url patern here 
    path('writer_login/',views.writer_login,name='writerlogin')

]