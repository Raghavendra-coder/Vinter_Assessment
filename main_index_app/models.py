from django.db import models
import uuid
# Create your models here.


class HealthProsperityIndexData(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    employment_total_population = models.IntegerField(null=True, blank=True)
    working_total_population = models.IntegerField(null=True, blank=True)
    real_estate_taxes_by_mortgage = models.FloatField(null=True, blank=True)
    household_income = models.FloatField(null=True, blank=True)
    severe_housing_problem = models.FloatField(null=True, blank=True)
    child_mortality_rate = models.FloatField(null=True, blank=True)
    working_average_wage = models.FloatField(null=True, blank=True)
    health_care_insurance = models.FloatField(null=True, blank=True)
    year = models.CharField(max_length=4, null=True, blank=True)
