from django.contrib import admin
from .models import Location, Profile, Organization, Degree, JobPost,\
Skill, Position, Setting, Concentration, Education, Experience, Bullet,\
UserSkillLevel, ResumeUpload

admin.site.register(Location)
admin.site.register(Profile)
admin.site.register(Organization)
admin.site.register(Degree)
admin.site.register(JobPost)
admin.site.register(Skill)
admin.site.register(Position)
admin.site.register(Setting)
admin.site.register(Concentration)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Bullet)
admin.site.register(UserSkillLevel)
admin.site.register(ResumeUpload)
