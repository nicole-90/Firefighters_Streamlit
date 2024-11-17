import streamlit as st
import plotly.express as px

# Title of the app
st.title("London Fire Brigade Incident & Mobilisation Data - Visualisation")

# Assuming the cleaned and merged data is passed from the first page
# You can load the cleaned data using the same method as on the first page
@st.cache_data
def load_cleaned_data():
    # Load the already cleaned and merged data from your storage or cache
    return pd.read_csv("cleaned_data.csv")  # Adjust this path if needed

# Load cleaned data
cleaned_data = load_cleaned_data()

# Display the cleaned dataset preview
st.header("Cleaned Data Preview")
st.write(cleaned_data.head())

# Add filter options for Year and Incident Group to the visualisation page
st.header("Filter the Data")
year_filter = st.selectbox("Select Year", options=sorted(cleaned_data['CalYear'].unique()), index=0)
incident_group_filter = st.selectbox("Select Incident Group", options=sorted(cleaned_data['IncidentGroup'].dropna().unique()), index=0)

# Filter the cleaned data based on the selected year and incident group
filtered_data = cleaned_data[(cleaned_data['CalYear'] == year_filter) & (cleaned_data['IncidentGroup'] == incident_group_filter)]

# Show filtered dataset preview
st.write(f"Filtered Dataset for Year: {year_filter} and Incident Group: {incident_group_filter}")
st.write(filtered_data.head())

# Visualisation 1: Incident Frequency by Year
st.header("Incident Frequency by Year")
incident_count_by_year = filtered_data.groupby('CalYear').size().reset_index(name='Incident Count')
fig_incident_by_year = px.bar(incident_count_by_year, x='CalYear', y='Incident Count', title='Incident Frequency by Year')
st.plotly_chart(fig_incident_by_year)

# Visualisation 2: Incident Group Distribution
st.header("Incident Group Distribution")
incident_group_count = filtered_data['IncidentGroup'].value_counts().reset_index(name='Count')
incident_group_count.columns = ['Incident Group', 'Count']
fig_incident_group = px.pie(incident_group_count, names='Incident Group', values='Count', title='Incident Group Distribution')
st.plotly_chart(fig_incident_group)

# Visualisation 3: Mobilisation Time vs Incident Type
st.header("Mobilisation Time vs Incident Type")
fig_mobilisation_time = px.scatter(filtered_data, x='MobilisationTime', y='IncidentGroup', color='IncidentGroup', 
                                   title="Mobilisation Time vs Incident Group")
st.plotly_chart(fig_mobilisation_time)

# Visualisation 4: Delay by Incident Type (if relevant column exists)
if 'DelayMinutes' in cleaned_data.columns:
    st.header("Delay by Incident Type")
    delay_by_incident_type = filtered_data.groupby('IncidentGroup')['DelayMinutes'].mean().reset_index(name='Average Delay (Minutes)')
    fig_delay_by_incident_type = px.bar(delay_by_incident_type, x='IncidentGroup', y='Average Delay (Minutes)', 
                                       title="Average Delay by Incident Group")
    st.plotly_chart(fig_delay_by_incident_type)

# Optionally, download the filtered dataset as CSV (to be used for further analysis or exporting)
st.header("Download Filtered Data")
st.text("Click the button below to download the filtered dataset.")
filtered_csv = filtered_data.to_csv(index=False)
st.download_button(label="Download Filtered Data (CSV)", data=filtered_csv, file_name="filtered_data.csv", mime="text/csv")

# Summary of visualisations
st.header("Summary of Visualisations")
visualisations_summary = """
1. **Incident Frequency by Year:**
   - Displays the total number of incidents reported each year, helping to identify trends over time.

2. **Incident Group Distribution:**
   - Pie chart showing the distribution of incident types within the selected year and group.

3. **Mobilisation Time vs Incident Type:**
   - Scatter plot showing the relationship between mobilisation time and incident group.

4. **Delay by Incident Group:**
   - Bar chart showing the average delay by incident type (if applicable).

5. **Filtered Data Download:**
   - You can download the filtered dataset for further analysis.

This page offers a comprehensive view of the data's trends and patterns, allowing for better insights into the London Fire Brigade's operations.
"""

# Display visualisation summary in a text area
st.text_area("Visualisation Summary", visualisations_summary, height=200)

