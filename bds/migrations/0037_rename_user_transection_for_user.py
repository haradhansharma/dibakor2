# Generated by Django 4.1.3 on 2022-12-05 17:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bds', '0036_transection_user_alter_transection_verified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transection',
            old_name='user',
            new_name='for_user',
        ),
    ]
