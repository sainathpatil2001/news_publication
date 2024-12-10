from django.urls import path,include
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('post_writer_home/', views.post_writer_home, name='post_writer_home'),
    path('write_post/',views.write_new_post,name='write_post')

]
