# Generated by Django 4.1.1 on 2022-10-04 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume_tailor', '0005_rename_consentrtion_consentration'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='loc',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='resume_tailor.location'),
        ),
    ]