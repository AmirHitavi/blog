# Generated by Django 5.0.1 on 2024-01-29 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_profile_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
