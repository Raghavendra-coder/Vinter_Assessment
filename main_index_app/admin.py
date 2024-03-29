from django.contrib import admin
from .models import HealthProsperityIndexData

# Register your models here.
@admin.register(HealthProsperityIndexData)
class HealthProsperityIndexDataAdmin(admin.ModelAdmin):
    list_display = ('year', 'employment_total_population',
                    'working_total_population', 'working_average_wage',
                    'health_care_insurance', 'real_estate_taxes_by_mortgage',
                    'household_income', 'severe_housing_problem', 'child_mortality_rate',
                    'health_care_insurance')
