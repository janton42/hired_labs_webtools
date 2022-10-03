from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Location

def home(request):
    return render(request, 'hired_labs_home.html')

def resume_tailor_home(request):
    return render(request,'resume_tailor_home.html')
