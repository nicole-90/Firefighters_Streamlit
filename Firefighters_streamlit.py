import streamlit as st
import pandas as pd
from functions import load_incident_data, load_mobilisation_data, clean_and_merge_data, drop_duplicates_and_columns, handle_missing_data

# Title of the app
st.title("London Fire Brigade Incident & Mobilisation Data")

# Load the data
st.header("Loading the Data")
st.text("This section loads the datasets: Incident Data (2009-2017, 2018 onwards) and Mobilisation Data (2009-2024).")

# Load incident and mobilization data from CSV and Excel
incidents = load_incident_data()
mobilisation = load_mobilisation_data()

# Display sample of loaded data
st.write("Incident data and Mobilization data loaded successfully.")

# Add filter options for Year and Incident Type
st.header("Filter the Data")
year_filter = st.selectbox("Select Year", options=sorted(incidents['Year'].unique()), index=0)
incident_type_filter = st.selectbox("Select Incident Type", options=sorted(incidents['IncidentType'].unique()), index=0)

# Filter the data based on the selected year and incident type
filtered_incidents = incidents[(incidents['Year'] == year_filter) & (incidents['IncidentType'] == incident_type_filter)]

# Show filtered dataset preview (first few rows)
st.write(f"Filtered Dataset for Year: {year_filter} and Incident Type: {incident_type_filter}")
st.write(filtered_incidents.head())

# Clean and merge data
st.header("Cleaning and Merging the Data")
st.text("Merging the incident and mobilization data on the IncidentNumber column.")
merged_data = clean_and_merge_data(filtered_incidents, mobilisation)

# Drop duplicates and unnecessary columns
st.header("Cleaning Data: Removing Duplicates & Unnecessary Columns")
cleaned_data = drop_duplicates_and_columns(merged_data)

# Handle missing data
st.header("Handling Missing Data")
st.text("Summarizing and dropping rows with missing values for critical columns.")
cleaned_data, missing_data_summary = handle_missing_data(cleaned_data)

# Display missing data summary
st.write("Missing Data Summary (Percentage and Count):")
st.write(missing_data_summary)

# Show cleaned dataset preview (first few rows)
st.write("Cleaned Dataset Preview (Top 5 rows):")
st.write(cleaned_data.head())

# Optionally, download the cleaned data as CSV
st.header("Download Cleaned Data")
st.text("Click the button below to download the cleaned dataset.")
csv = cleaned_data.to_csv(index=False)
st.download_button(label="Download Cleaned Data (CSV)", data=csv, file_name="cleaned_data.csv", mime="text/csv")

# Summary of changes made to the dataset
st.header("Summary of Changes Made to the Dataset")
changes_summary = """
1. **Data Loaded:**
   - Incident data (2009-2017 and 2018 onwards) and Mobilization data (2009-2024) loaded successfully from CSV and Excel files.

2. **Data Cleaning:**
   - Duplicates were removed based on the 'IncidentNumber' column. Only the first occurrence of each incident was kept.
   - Unnecessary columns like 'DelayCode_Description', 'Notional Cost (£)', and other irrelevant fields were dropped to simplify the dataset.

3. **Missing Data Handling:**
   - Missing values in critical columns were handled. Rows with missing 'USRN' values were dropped.
   - A summary of the missing data (percentage and count) was displayed for transparency.

4. **Merged Data:**
   - Incident data and Mobilization data were merged successfully based on the 'IncidentNumber' column.

5. **Cleaned Data:**
   - The final dataset has been cleaned and is now ready for analysis. It includes all relevant columns and is free from duplicates and excessive missing data.
"""

# Display changes summary in a text area
st.text_area("Changes Summary", changes_summary, height=200)
