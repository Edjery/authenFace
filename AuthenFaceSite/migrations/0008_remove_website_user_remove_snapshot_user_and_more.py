# Generated by Django 5.0.1 on 2024-01-30 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenFaceSite', '0007_alter_snapshot_created_at_alter_website_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='website',
            name='user',
        ),
        migrations.RemoveField(
            model_name='snapshot',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
        migrations.DeleteModel(
            name='Website',
        ),
        migrations.DeleteModel(
            name='AuthenFaceUser',
        ),
        migrations.DeleteModel(
            name='Snapshot',
        ),
    ]
