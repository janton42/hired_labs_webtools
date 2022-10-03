from django.urls import path

from . import views

urlpatterns = [
    path('', views.resume_tailor_home, name='resume_tailor_home'),
]
