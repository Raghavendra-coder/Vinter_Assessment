import time

import pandas as pd
import requests
import os
import streamlit as st
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_prosperity_index.settings')
django.setup()
from main_index_app.models import HealthProsperityIndexData


def insert_data(field_name, data: dict = dict()):
    for key, value in data.items():
        try:
            instance = HealthProsperityIndexData.objects.get(year=key)
            setattr(instance, field_name, value)
        except HealthProsperityIndexData.DoesNotExist:
            instance = HealthProsperityIndexData(**{"year": key, field_name: value})
        instance.save()


def employment_data():
    # EMPLOYMENT
    # ID Year', 'Year', 'ID Gender', 'Gender', 'ID Age', 'Age',
    #        'ID Workforce Status', 'Workforce Status', 'Total Population',
    #        'Geography', 'ID Geography', 'Slug Geography'
    employment_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=Year,Gender,Age&measures=Total Population&Geography=01000US&Workforce Status=true")
    employment_df = pd.DataFrame.from_records(employment_response.json()["data"])
    return_df = employment_df.groupby("Year")["Total Population"].agg(["sum"]).rename(
        columns={"sum": "Total working Population"})
    return_dict = return_df.to_dict()["Total working Population"]
    insert_data("employment_total_population", return_dict)


def working_population_data():
    # WORKING POPULATION
    # 'ID Age', 'Age', 'ID Gender', 'Gender', 'ID Group', 'Group', 'ID Year',
    #        'Year', 'Total Population', 'Total Population MOE Appx', 'Average Wage',
    #        'Average Wage Appx MOE', 'Geography', 'ID Geography', 'Slug Geography'
    working_population_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US&drilldowns=Age,Gender,Group,Year&measures=Total Population,Total Population MOE Appx,Average Wage,Average Wage Appx MOE")
    working_population_df = pd.DataFrame.from_records(working_population_response.json()["data"])
    return_working_population_df = working_population_df.groupby("Year")["Total Population"].agg(["sum"]).rename(
        columns={"sum": "Working Population"})
    return_avg_wage_df = working_population_df.groupby("Year")["Average Wage"].mean()
    return_df = pd.concat([return_working_population_df, return_avg_wage_df], axis=1)
    dict1 = return_avg_wage_df.to_dict()
    dict2 = return_working_population_df.to_dict()["Working Population"]
    insert_data("working_average_wage", dict1)
    insert_data("working_total_population", dict2)


def housing_data():
    # HOUSING
    # 'ID Real Estate Taxes Paid', 'Real Estate Taxes Paid', 'ID Year',
    #        'Year', 'Real Estate Taxes by Mortgage',
    #        'Real Estate Taxes by Mortgage Moe', 'Geography', 'ID Geography',
    #        'Slug Geography'
    housing_response = requests.get("https://zircon.datausa.io/api/data?measure=Year,Real Estate Taxes by Mortgage,Real Estate Taxes by Mortgage Moe&Geography=01000US,01000US&drilldowns=Real Estate Taxes Paid")
    housing_df = pd.DataFrame.from_records(housing_response.json()["data"])
    return_df = housing_df.groupby("Year")["Real Estate Taxes by Mortgage"].agg(["sum"]).rename(
        columns={"sum": "Real Estate Taxes by Mortgage"})
    return_dict = return_df.to_dict()["Real Estate Taxes by Mortgage"]
    insert_data("real_estate_taxes_by_mortgage", return_dict)


def equity_data():
    # EQUITY
    # ID Race', 'Race', 'ID State', 'State', 'ID Year', 'Year',
    #        'Household Income by Race', 'Household Income by Race Moe',
    #        'Slug State
    equity_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US:children&measure=Household Income by Race,Household Income by Race Moe&drilldowns=Race")
    equity_df = pd.DataFrame.from_records(equity_response.json()["data"])
    return_df = equity_df.groupby("Year")["Household Income by Race"].agg(["sum"]).rename(
        columns={"sum": "Household Income by Race"})
    return_dict = return_df.to_dict()["Household Income by Race"]
    insert_data("household_income", return_dict)


def poverty_data():
    # POVERTY
    # ID State', 'State', 'ID Year', 'Year', 'Severe Housing Problems',
    #        'Severe Housing Problems CI Low', 'Severe Housing Problems CI High',
    #        'Slug State'
    poverty_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=State,Year&measures=Severe Housing Problems,Severe Housing Problems CI Low,Severe Housing Problems CI High")
    poverty_df = pd.DataFrame.from_records(poverty_response.json()["data"])
    return_df = poverty_df.groupby("Year")["Severe Housing Problems"].agg(["sum"]).rename(
        columns={"sum": "Severe Housing Problems"})
    return_dict = return_df.to_dict()["Severe Housing Problems"]
    insert_data("severe_housing_problem", return_dict)


def health_care_data():
    # Health Care Diversity
    # ID Year', 'Year', 'ID Health Coverage', 'Health Coverage', 'ID Gender',
    #        'Gender', 'Health Insurance by Gender and Age', 'Geography',
    #        'ID Geography', 'Slug Geography
    health_care_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US&drilldowns=Year,Health Coverage,Gender&measures=Health Insurance by Gender and Age")
    health_care_response_df = pd.DataFrame.from_records(health_care_response.json()["data"])
    return_df = health_care_response_df.groupby("Year")["Health Insurance by Gender and Age"].agg(["sum"]).rename(
        columns={"sum": "Health Insurance by Gender and Age"})
    return_dict = return_df.to_dict()["Health Insurance by Gender and Age"]
    insert_data("health_care_insurance", return_dict)


def child_mortality_data():
    # child mortality
    # ID State', 'State', 'ID Year', 'Year', 'Child Mortality',
    #        'Child Mortality CI Low', 'Child Mortality CI High', 'Slug State'
    child_mortality_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=State,Year&measures=Child Mortality,Child Mortality CI Low,Child Mortality CI High")
    child_mortality_df = pd.DataFrame.from_records(child_mortality_response.json()["data"])
    return_df = child_mortality_df.groupby("Year")["Child Mortality"].agg(["sum"]).rename(
        columns={"sum": "Child Mortality"})
    return_dict = return_df.to_dict()["Child Mortality"]
    insert_data("child_mortality_rate", return_dict)


def main(add=False):
    if add:
        bar = st.progress(0)
    employment_data()
    if add:
        bar.progress(14)
    working_population_data()
    if add:
        bar.progress(28)
    housing_data()
    if add:
        bar.progress(42)
    equity_data()
    if add:
        bar.progress(56)
    poverty_data()
    if add:
        bar.progress(70)
    health_care_data()
    if add:
        bar.progress(85)
    child_mortality_data()
    if add:
        bar.progress(100)
        st.write("Database update complete")
        time.sleep(2)


if __name__ == '__main__':
    main()
