# Generated by Django 5.0.2 on 2024-05-15 22:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_client_alter_event_organiser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='cat_image',
            new_name='thmbnail',
        ),
    ]
