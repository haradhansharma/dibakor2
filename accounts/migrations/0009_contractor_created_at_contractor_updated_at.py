# Generated by Django 4.1.3 on 2022-12-12 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_user_is_contractor_contractor'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractor',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='contractor',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]