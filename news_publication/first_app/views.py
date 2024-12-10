from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django import forms
from .models import Writer
from django.shortcuts import render, get_object_or_404, redirect


# Custom Signup Form with Email Field
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

# Home View (Requires Login)
@login_required
def home(request):
    return render(request, 'first_app/home.html', {'user': request.user})

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after signup
            messages.success(request, "Signup successful! You are now logged in.")
            return redirect('home')
        else:
            messages.error(request, "Signup failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'first_app/signup.html', {'form': form})

from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'first_app/login.html'

    # Overriding form_valid to add success message
    def form_valid(self, form):
        messages.success(self.request, "Login successful!")
        return super().form_valid(form)

    # Overriding form_invalid to add error message
    def form_invalid(self, form):
        messages.error(self.request, "Login failed. Please try again.")
        return super().form_invalid(form)

    # Passing the logged-in user's email to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_email'] = self.request.user.email  # Pass the email to the context
        return context


# Custom Logout View
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You have been logged out.")
        return super().dispatch(request, *args, **kwargs)

#post writer view
from django.shortcuts import render, redirect
from django.http import HttpResponse
from first_app.models import Writer
from .forms import WriterLoginForm

def writer_login(request):
    if request.method == 'POST':
        form = WriterLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if the writer exists in the database
            try:
                writer = Writer.objects.get(username=username, password=password)
                # Login successful, store the username in session
                request.session['username'] = username
                return redirect('post_writer_home')  # Redirect to post_writer_home view
            except Writer.DoesNotExist:
                # Invalid credentials
                return HttpResponse("Invalid username or password", status=401)
    else:
        form = WriterLoginForm()

    return render(request, 'first_app/writer_login.html', {'form': form})



from django.shortcuts import render
from django.http import JsonResponse
from .models import Writer

def add_writer_login(request):
    # If it's an AJAX request for search, filter writers
    search_query = request.GET.get('search', '')
    if search_query:
        writers = Writer.objects.filter(username__icontains=search_query)
    else:
        writers = Writer.objects.all()
        
    return render(request, 'first_app/add_writer_login.html', {'writers': writers})

def search_writers(request):
    search_query = request.GET.get('search', '')
    if search_query:
        writers = Writer.objects.filter(username__icontains=search_query)
    else:
        writers = Writer.objects.all()
        
    writers_data = [{'id': writer.id, 'username': writer.username, 'first_name': writer.first_name, 'last_name': writer.last_name} for writer in writers]
    
    return JsonResponse({'writers': writers_data})


def update_writer(request, id):
    writer = get_object_or_404(Writer, id=id)
    
    if request.method == 'POST':
        writer.first_name = request.POST.get('first_name')
        writer.last_name = request.POST.get('last_name')
        writer.password = request.POST.get('password')  # Insecure for real apps
        writer.save()
        return redirect('add_writer_login')

    return render(request, 'first_app/update_writer.html', {'writer': writer})


def delete_writer(request, id):
    writer = get_object_or_404(Writer, id=id)
    writer.delete()
    return redirect('add_writer_login')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Writer

def add_writer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validate fields
        if not username or not password or not first_name or not last_name:
            messages.error(request, "All fields are required.")
            return render(request, 'first_app/add_writer.html')

        # Check for duplicate username
        if Writer.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'first_app/add_writer.html')

        # Save writer to database
        Writer.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        messages.success(request, "Writer added successfully.")
        return redirect('add_writer_login')  # Redirect to the writers list view (or another page)

    return render(request, 'first_app/add_writer.html')

