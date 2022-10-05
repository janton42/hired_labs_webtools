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

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    loc = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    phone = models.IntegerField()
    linkedin = models.CharField(max_length=300)

    def __str__(self):
        return '{}: {} '\
        .format(\
        self.user.id,
        self.user.get_full_name(),
        )

class Organization(models.Model):
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    sector = models.CharField(max_length=250)
    size = models.CharField(max_length=250)
    loc = models.ForeignKey(Location, on_delete=models.CASCADE,default=1,null=True)

    def __str__(self):
        return self.name

class Degree(models.Model):
    name = models.CharField(max_length=250)
    abbr = models.CharField(max_length=4)


    def __str__(self):
        return '{}: {}'.format(self.abbr, self.name)

class JobPost(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.SET_NULL,null=True)
    title = models.CharField(max_length=200)
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    text = models.TextField()
    unigrams = models.TextField()
    bigrams = models.TextField()
    trigrams = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.title, self.org)

class Skill(models.Model):
    SKILL_TYPES = [
        ('Hard','Hard'),
        ('Soft','Soft')
    ]
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=4, choices=SKILL_TYPES)
    feild = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Position(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Setting(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=True)

    def __str__(self):
        return self.user.user.get_full_name()

    def get_queryset(self):
        return self.model.objects.all().filter(issuer=self.request.user)

class Concentration(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    def get_queryset(self):
        return self.model.objects.all().filter(issuer=self.request.user)

class Education(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    grad_date = models.DateField()
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    concentration = models.ForeignKey(Concentration, on_delete=models.CASCADE)

    def __str__(self):
        return  '{}: {}, {} - {}'.format(\
        self.user.user.get_full_name(),\
        self.org, self.degree, self.concentration)

    def get_queryset(self):
        return self.model.objects.all().filter(issuer=self.request.user)

class Experience(models.Model):
    EXP_LABELS = [
        ('Work','Work'),
        ('Leadership','Leadership'),
    ]
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    label = models.CharField(max_length=20, choices=EXP_LABELS)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    loc = models.ForeignKey(Location, on_delete=models.SET_NULL,null=True)
    on_current = models.BooleanField(default=True)

    def __str__(self):
        return  '{}: {}'.format(\
        self.org, self.position)

    def get_queryset(self):
        return self.model.objects.all().filter(issuer=self.request.user)

class Bullet(models.Model):
    BULLET_TYPES = [
        ('Work','Work'),
        ('Summary','Summary')
    ]
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=BULLET_TYPES)

    def __str__(self):
        return '{}: {}, {}'.format(self.id, self.text, self.experience)

    def get_queryset(self):
        return self.model.objects.all().filter(issuer=self.request.user)

class UserSkillLevel(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.IntegerField()

    def __str__(self):
        return '{}: {}, {}'.format(self.user, self.skill, self.level)

class ResumeUpload(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    resume = models.FileField(upload_to='uploads/')

    def __str__(self):
        return '{}: {}'.format(self.user, self.title)
