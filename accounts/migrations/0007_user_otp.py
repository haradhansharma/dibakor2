# Generated by Django 4.1.3 on 2022-11-28 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_profile_profile_photo_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(default='', max_length=6),
            preserve_default=False,
        ),
    ]