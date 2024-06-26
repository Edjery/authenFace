# Generated by Django 5.0.3 on 2024-03-28 04:12

import API.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0007_remove_authenfaceuser_userimagename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenfaceuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=API.models.renameImage),
        ),
        migrations.AlterField(
            model_name='snapshot',
            name='image',
            field=models.ImageField(upload_to='Snapshots/'),
        ),
    ]
