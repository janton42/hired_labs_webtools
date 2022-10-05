from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UpdateProfileForm

from .models import Location, Setting

def home(request):
    return render(request, 'hired_labs_home.html')

def register(request):
    if request.method =='POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, 'Your account has been created.\n\
            You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'register.html', context)

@login_required
def resume_tailor_home(request):
    return render(request,'resume_tailor_home.html')

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_view',pk=profile.pk)
    else:
        form = UpdateProfileForm()
    context = { 'form': form }
    return render(request, 'profile_update.html', context)
