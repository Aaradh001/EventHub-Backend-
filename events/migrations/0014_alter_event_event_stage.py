# Generated by Django 5.0.2 on 2024-05-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_remove_event_status_event_venue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_stage',
            field=models.CharField(blank=True, choices=[('LAUNCHED', 'LAUNCHED'), ('VENUE-SELECTION', 'VENUE-SELECTION'), ('REQUIREMENT-SELECTION', 'REQUIREMENT-SELECTION'), ('VENDOR-SELECTION', 'VENDOR-SELECTION'), ('ADVANCE-PAYMENT', 'ADVANCE-PAYMENT'), ('BOOKED', 'BOOKED'), ('WORK_IN_PROGRESS', 'WORK_IN_PROGRESS'), ('VERIFICATION_IN_PROGRESS', 'VERIFICATION_IN_PROGRESS'), ('COMPLETED', 'COMPLETED'), ('CANCELLED_BY_CLIENT', 'CANCELLED_BY_CLIENT'), ('CANCELLED_BY_ADMIN', 'CANCELLED_BY_ADMIN')], default='LAUNCHED', max_length=200, null=True),
        ),
    ]
