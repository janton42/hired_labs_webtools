from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegistrationForm, UpdateProfileForm, \
UploadFileForm

from .models import Location, Setting, Profile, ResumeUpload

from .packages.resume_parser.main import ResumeParser
# Home page (home) and Registration page (register) are the only pages
# accessible without a login.

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

# All views below should require login

@login_required
def resume_tailor_home(request):
    resumes = ResumeUpload.objects.all()\
    .filter(user=request.user)\
    .values()
    context = {
        'resumes': resumes
    }
    return render(request,'resume_tailor_home.html', context)

@login_required
def profile(request):
    user_profile = Profile.objects.all()\
    .filter(user=request.user)\
    .values()
    context = { 'user_profile': user_profile }
    return render(request, 'profile.html', context)

@login_required
def settings(request):
    user_settings = Setting.objects.all()\
    .filter(user__user=request.user)\
    .values()
    context = { 'user_settings': user_settings }
    return render(request, 'settings.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile.html',pk=profile.pk)
    else:
        form = UpdateProfileForm()
    context = { 'form': form }
    return render(request, 'profile_update.html', context)

@login_required
def upload_resume(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.save()
            return redirect('resume_tailor_home')
        else:
            print(form.errors)
    else:
        form = UploadFileForm()
    context = { 'form': form }
    return render(request, 'resume_upload.html', context)

@login_required
def parsed_resume(request, resume_id):
    resume = ResumeUpload.objects.all()\
    .filter(id=resume_id)\
    .values()
    for r in resume:
        # Initialize a parcer instance named after the current user
        parser = ResumeParser(name=request.user)
        # Make a folder for this user, if one doesn't already exist,
        # get the full path to the selected resume file to be parsed,
        # and get the uploaded file's extension
        parser.get_resume_paths(r['resume'])
        # Print instance attributes out to the consol
        # parser.introduce_self()
        parser.read_resume()
    context = {
        'resume': resume
    }
    return render(request, 'parsed.html', context)
