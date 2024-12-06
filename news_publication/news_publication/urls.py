from django.contrib import admin
from django.urls import path,include
from django.shortcuts import render, redirect

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',include('first_app.urls')),
     path('post_writer/', include('post_writer.urls')),  # URLs for post_writer app
    
]
