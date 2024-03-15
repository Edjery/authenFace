# Generated by Django 5.0.2 on 2024-03-15 01:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_authenfaceuser_userimagename_delete_userimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapshot',
            name='image',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='snapshots/'),
            preserve_default=False,
        ),
    ]