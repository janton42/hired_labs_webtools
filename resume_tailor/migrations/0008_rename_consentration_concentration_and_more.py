# Generated by Django 4.1.1 on 2022-10-05 00:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume_tailor', '0007_education_user_experience_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Consentration',
            new_name='Concentration',
        ),
        migrations.RenameField(
            model_name='education',
            old_name='consentration',
            new_name='concentration',
        ),
    ]
