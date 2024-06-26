# Generated by Django 5.0.2 on 2024-05-11 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue_management', '0003_alter_venue_add_line_1_alter_venue_add_line_2'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='full_address',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='add_line_2',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='lat_long',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='venue',
            name='street',
            field=models.CharField(blank=True, db_index=True, default='', max_length=300, null=True),
        ),
    ]
