# Generated by Django 5.0.2 on 2024-04-10 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_baseservices_normal_cost_per_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseservices',
            name='unit_of_measurement',
            field=models.CharField(choices=[('PERSON_COUNT', 'PERSON_COUNT'), ('SQUARE_FEET', 'SQUARE_FEET')], default='PERSON_COUNT', max_length=100),
        ),
    ]
