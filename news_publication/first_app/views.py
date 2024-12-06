from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django import forms

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
