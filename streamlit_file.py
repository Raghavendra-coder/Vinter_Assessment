import numpy as np
import pandas as pd
import streamlit as st
import os

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from main_index_app.models import HealthProsperityIndexData


def create_dataframe():
    q = HealthProsperityIndexData.objects.all().order_by("year").values('year', 'employment_total_population',
                                                       'working_total_population',
                                                       'real_estate_taxes_by_mortgage',
                                                       'household_income', 'severe_housing_problem',
                                                       'child_mortality_rate', 'working_average_wage',
                                                       'health_care_insurance')
    if not q:
        st.write("There is no data in database. Please wait we are updating the database")
        from add_data import main
        main(add=True)
        q = HealthProsperityIndexData.objects.all().values('year', 'employment_total_population',
                                                           'working_total_population',
                                                           'real_estate_taxes_by_mortgage',
                                                           'household_income', 'severe_housing_problem',
                                                           'child_mortality_rate', 'working_average_wage',
                                                           'health_care_insurance')
    df = pd.DataFrame.from_records(q)
    return df


def add_prosperity_index():
    final_data = create_dataframe()
    # Normalize each column to a 0-100 scale

    required_columns = final_data.columns.tolist()
    required_columns.remove("year")
    for column in required_columns:  # Skipping the 'Year' column for normalization
        final_data[column] = ((final_data[column] - final_data[column].min()) /
                                       (final_data[column].max() - final_data[column].min())) * 100

    # Adjust weights to include the new variable: now 8 variables, so each gets a weight of 1/8
    weights_with_wage = np.array([1/8] * 8)  # Equal weights for each of the 8 variables
    # Calculate the Health and Prosperity Index with the new variable included
    final_data['Health and Prosperity Index'] = final_data.loc[:, required_columns].dot(weights_with_wage)

    return final_data


def main():
    final_data_with_index = add_prosperity_index()
    st.line_chart(final_data_with_index.loc[:, ['year', 'Health and Prosperity Index']],
                  x="year", y="Health and Prosperity Index")

    st.dataframe(final_data_with_index.loc[:, ['year', 'Health and Prosperity Index']])


if __name__ == '__main__':
    main()
