from django.urls import path

from . import views

urlpatterns = [
    path('', views.resume_tailor_home, name='resume_tailor_home'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/settings/', views.settings, name='settings'),
    path('upload_resume/', views.upload_resume, name='upload_resume'),
    path('parsed/<int:resume_id>', views.parsed_resume, name='parsed'),
]
