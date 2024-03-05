# Generated by Django 5.0.2 on 2024-03-04 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_authenfaceuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='authenfaceuser',
            name='userImageName',
            field=models.CharField(default='SampleImage', max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='UserImage',
        ),
    ]
