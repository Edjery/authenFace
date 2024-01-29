# Generated by Django 5.0.1 on 2024-01-29 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenFaceSite', '0004_alter_authenfaceuser_id_alter_snapshots_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Snapshots',
            new_name='Snapshot',
        ),
        migrations.RenameModel(
            old_name='Websites',
            new_name='Website',
        ),
        migrations.RenameField(
            model_name='snapshot',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='userimage',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='userId',
            new_name='user',
        ),
    ]
