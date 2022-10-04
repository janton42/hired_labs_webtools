from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=85)
    country = models.CharField(max_length=60)

    def __str__(self):
        return '{}, {}, {}'\
        .format(\
        self.country,\
        self.state,\
        self.city\
        )

# class ProfileManager(models.Manager):
#     def update_profile(self, user, loc, phone, linkedin):
#         profile = self.get_or_create(\
#         user = user, loc = loc, phone = phone, linkedin = linkedin)
#         return profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loc = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    phone = models.IntegerField()
    linkedin = models.CharField(max_length=300)

    # objects = ProfileManager()

    def __str__(self):
        return '{}: {} '\
        .format(\
        self.user.id,
        self.user.get_full_name(),
        )
