# Generated by Django 4.2.11 on 2024-03-28 20:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HealthProsperityIndexData',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=26, primary_key=True, serialize=False, unique=True)),
                ('employment_total_population', models.IntegerField(blank=True, default=0, null=True)),
                ('working_total_population', models.IntegerField(blank=True, default=0, null=True)),
                ('real_estate_taxes_by_mortage', models.FloatField(blank=True, default=0.0, null=True)),
                ('household_income', models.FloatField(blank=True, default=0.0, null=True)),
                ('severe_housing_problem', models.FloatField(blank=True, default=0.0, null=True)),
                ('child_mortality_rate', models.FloatField(blank=True, default=0.0, null=True)),
                ('working_average_wage', models.FloatField(blank=True, default=0.0, null=True)),
                ('year', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]
