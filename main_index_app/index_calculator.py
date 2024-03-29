import numpy as np
import pandas as pd
import requests
import streamlit as st


def employment_data():
    # EMPLOYMENT
    # ID Year', 'Year', 'ID Gender', 'Gender', 'ID Age', 'Age',
    #        'ID Workforce Status', 'Workforce Status', 'Total Population',
    #        'Geography', 'ID Geography', 'Slug Geography'
    employment_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=Year,Gender,Age&measures=Total Population&Geography=01000US&Workforce Status=true")
    employment_df = pd.DataFrame.from_records(employment_response.json()["data"])
    return_df = employment_df.groupby("Year")["Total Population"].agg(["sum"]).rename(
        columns={"sum": "Total working Population"})
    return return_df


def working_population_data():
    # WORKING POPULATION
    # 'ID Age', 'Age', 'ID Gender', 'Gender', 'ID Group', 'Group', 'ID Year',
    #        'Year', 'Total Population', 'Total Population MOE Appx', 'Average Wage',
    #        'Average Wage Appx MOE', 'Geography', 'ID Geography', 'Slug Geography'
    working_population_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US&drilldowns=Age,Gender,Group,Year&measures=Total Population,Total Population MOE Appx,Average Wage,Average Wage Appx MOE")
    working_population_df = pd.DataFrame.from_records(working_population_response.json()["data"])
    return_working_population_df = working_population_df.groupby("Year")["Total Population"].agg(["sum"])
    return_avg_wage_df = working_population_df.groupby("Year")["Average Wage"].mean()
    return_df = pd.concat([return_working_population_df, return_avg_wage_df], axis=1).rename(
        columns={"sum": "Working Population"})
    return return_df


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
    return return_df


def equity_data():
    # EQUITY
    # ID Race', 'Race', 'ID State', 'State', 'ID Year', 'Year',
    #        'Household Income by Race', 'Household Income by Race Moe',
    #        'Slug State
    equity_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US:children&measure=Household Income by Race,Household Income by Race Moe&drilldowns=Race")
    equity_df = pd.DataFrame.from_records(equity_response.json()["data"])
    return_df = equity_df.groupby("Year")["Household Income by Race"].agg(["sum"]).rename(
        columns={"sum": "Household Income by Race"})
    return return_df


def poverty_data():
    # POVERTY
    # ID State', 'State', 'ID Year', 'Year', 'Severe Housing Problems',
    #        'Severe Housing Problems CI Low', 'Severe Housing Problems CI High',
    #        'Slug State'
    poverty_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=State,Year&measures=Severe Housing Problems,Severe Housing Problems CI Low,Severe Housing Problems CI High")
    poverty_df = pd.DataFrame.from_records(poverty_response.json()["data"])
    return_df = poverty_df.groupby("Year")["Severe Housing Problems"].agg(["sum"]).rename(
        columns={"sum": "Severe Housing Problems"})
    return return_df


def health_care_data():
    # Health Care Diversity
    # ID Year', 'Year', 'ID Health Coverage', 'Health Coverage', 'ID Gender',
    #        'Gender', 'Health Insurance by Gender and Age', 'Geography',
    #        'ID Geography', 'Slug Geography
    health_care_response = requests.get("https://zircon.datausa.io/api/data?Geography=01000US&drilldowns=Year,Health Coverage,Gender&measures=Health Insurance by Gender and Age")
    health_care_response_df = pd.DataFrame.from_records(health_care_response.json()["data"])
    return_df = health_care_response_df.groupby("Year")["Health Insurance by Gender and Age"].agg(["sum"]).rename(
        columns={"sum": "Health Insurance by Gender and Age"})
    return return_df


def child_mortality_data():
    # child mortality
    # ID State', 'State', 'ID Year', 'Year', 'Child Mortality',
    #        'Child Mortality CI Low', 'Child Mortality CI High', 'Slug State'
    child_mortality_response = requests.get("https://zircon.datausa.io/api/data?drilldowns=State,Year&measures=Child Mortality,Child Mortality CI Low,Child Mortality CI High")
    child_mortality_df = pd.DataFrame.from_records(child_mortality_response.json()["data"])
    return_df = child_mortality_df.groupby("Year")["Child Mortality"].agg(["sum"]).rename(
        columns={"sum": "Child Mortality"})
    return return_df


def get_final_data():
    employment_df = employment_data()
    working_population_df = working_population_data()
    housing_df = housing_data()
    equity_df = equity_data()
    poverty_df = poverty_data()
    health_care_df = health_care_data()
    child_mortality_df = child_mortality_data()
    final_data = pd.concat([employment_df, working_population_df, housing_df, equity_df,
                            poverty_df, health_care_df, child_mortality_df], axis=1)
    final_data = final_data.reset_index()
    final_data.rename(columns={"index": "Year"}, inplace=True)

    return final_data


def add_prosperity_index():
    final_data = get_final_data()
    st.dataframe(final_data)
    # Normalize each column to a 0-100 scale, including the new "Working Average Wage"
    for column in final_data.columns[1:]:  # Skipping the 'Year' column for normalization
        final_data[column] = ((final_data[column] - final_data[column].min()) /
                                       (final_data[column].max() - final_data[column].min())) * 100

    # Adjust weights to include the new variable: now 8 variables, so each gets a weight of 1/8
    weights_with_wage = np.array([1/8] * 8)  # Equal weights for each of the 8 variables
    # Calculate the Health and Prosperity Index with the new variable included
    final_data['Health and Prosperity Index'] = final_data.iloc[:, 1:].dot(weights_with_wage)

    return final_data


def main():
    final_data_with_index = add_prosperity_index()
    st.line_chart(final_data_with_index.loc[:, ['Year', 'Health and Prosperity Index']],
                  x="Year", y="Health and Prosperity Index")
    st.dataframe(final_data_with_index)


if __name__ == '__main__':
    main()
