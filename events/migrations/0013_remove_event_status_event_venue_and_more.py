# Generated by Django 5.0.2 on 2024-05-19 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_event_event_stage_alter_event_status'),
        ('venue_management', '0008_venue_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='status',
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='venue_management.venue'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_stage',
            field=models.CharField(blank=True, choices=[('VENUE-SELECTION', 'VENUE-SELECTION'), ('REQUIREMENT-SELECTION', 'REQUIREMENT-SELECTION'), ('VENDOR-SELECTION', 'VENDOR-SELECTION'), ('ADVANCE-PAYMENT', 'ADVANCE-PAYMENT'), ('BOOKED', 'BOOKED'), ('WORK_IN_PROGRESS', 'WORK_IN_PROGRESS'), ('VERIFICATION_IN_PROGRESS', 'VERIFICATION_IN_PROGRESS'), ('COMPLETED', 'COMPLETED')], max_length=200, null=True),
        ),
    ]
