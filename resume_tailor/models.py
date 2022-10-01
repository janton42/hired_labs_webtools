from django.db import models

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
