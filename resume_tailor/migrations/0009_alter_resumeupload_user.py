# Generated by Django 4.1.1 on 2022-11-14 22:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('resume_tailor', '0008_rename_consentration_concentration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumeupload',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
