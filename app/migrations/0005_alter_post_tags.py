# Generated by Django 5.0.1 on 2024-01-30 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_post_slug_alter_tag_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='post', to='app.tag'),
        ),
    ]
