# Generated by Django 5.0.2 on 2024-05-05 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_otherservices_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherservices',
            name='unit_of_measurement',
            field=models.CharField(blank=True, choices=[('PERSON_COUNT', 'PERSON_COUNT'), ('COUNT', 'COUNT'), ('AREA(Sq_Ft)', 'AREA(Sq_Ft)')], default='PERSON_COUNT', max_length=100, null=True),
        ),
    ]