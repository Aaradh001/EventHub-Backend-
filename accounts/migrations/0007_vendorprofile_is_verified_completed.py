# Generated by Django 5.0.2 on 2024-04-11 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_otherservices_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendorprofile',
            name='is_verified_completed',
            field=models.BooleanField(default=False),
        ),
    ]
