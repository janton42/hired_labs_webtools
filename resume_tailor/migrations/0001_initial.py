# Generated by Django 4.1.1 on 2022-10-01 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=60)),
                ('state', models.CharField(max_length=85)),
                ('country', models.CharField(max_length=60)),
            ],
        ),
    ]