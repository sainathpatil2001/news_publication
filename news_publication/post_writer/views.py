# Create your views here.
from django.shortcuts import render
from first_app.models import Writer
from django.shortcuts import render, HttpResponse
from first_app.models import Writer


#first view to post write with writer detail accses 

def post_writer_home(request):
    # Get the username from session (if logged in)
    username = request.session.get('username')
    
    if username:
        try:
            # Fetch the writer data based on the username
            writer = Writer.objects.get(username=username)
            # Pass the writer's data to the template (not a list)
            return render(request, 'post_writer/post_writer_home.html', {'writer': writer})
        except Writer.DoesNotExist:
            return HttpResponse("Writer not found.", status=404)
    else:
        return HttpResponse("You need to log in first.", status=401)


def write_new_post(request):



    return render(request,'post_writer/new_post_write.html')