# Generated by Django 3.1.5 on 2021-01-30 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0004_articles_spheres'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='body',
            field=models.TextField(default='none'),
            preserve_default=False,
        ),
    ]
