# Generated by Django 5.0.2 on 2024-02-28 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_snapshot_user_alter_website_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenfaceuser',
            name='name',
            field=models.CharField(default='Username', max_length=100),
            preserve_default=False,
        ),
    ]
