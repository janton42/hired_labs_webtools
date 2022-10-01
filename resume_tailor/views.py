from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import Location

def index(request):
    return render(request,'resume_tailor/index.html')
