# Generated by Django 5.0.2 on 2024-04-08 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'verbose_name': 'EventCategory', 'verbose_name_plural': 'Event Categories'},
        ),
        migrations.AddField(
            model_name='eventcategory',
            name='cat_image',
            field=models.ImageField(blank=True, null=True, upload_to='events/event-categories/'),
        ),
    ]
