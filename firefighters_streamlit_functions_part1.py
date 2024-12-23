import pandas as pd
import pickle

def load_incident_data():
    """
    Load incident data from pickle file.
    Returns: 
        - incidents: A DataFrame containing the combined incident data.
    """
    with open('data/incidents.pkl', 'rb') as f:
        incidents = pickle.load(f)
    return incidents

def load_mobilisation_data():
    """
    Load mobilization data from pickle file.
    Returns: 
        - mobilisation: A DataFrame containing the combined mobilization data.
    """
    with open('data/mobilisation.pkl', 'rb') as f:
        mobilisation = pickle.load(f)
    return mobilisation

def clean_and_merge_data(incidents, mobilisation):
    """
    Clean and merge incident and mobilization data on 'IncidentNumber'.
    
    Params:
        - incidents: DataFrame containing incident data.
        - mobilisation: DataFrame containing mobilization data.
        
    Returns:
        - merged_data: DataFrame with merged incident and mobilization data.
    """
    incidents['IncidentNumber'] = incidents['IncidentNumber'].astype(str).str.strip().str.split('.').str[0]
    mobilisation['IncidentNumber'] = mobilisation['IncidentNumber'].astype(str).str.strip().str.split('.').str[0]

    # Merge the datasets on 'IncidentNumber'
    merged_data = pd.merge(incidents, mobilisation, on='IncidentNumber', how='outer')

    return merged_data

def drop_duplicates_and_columns(merged_data):
    """
    Remove duplicates based on 'IncidentNumber' and drop unnecessary columns.
    
    Params:
        - merged_data: DataFrame with incident and mobilization data merged.
        
    Returns:
        - cleaned_data: DataFrame with duplicates removed and unnecessary columns dropped.
    """
    # Remove duplicates
    cleaned_data = merged_data.drop_duplicates(subset=['IncidentNumber'], keep='first')

    # Columns to drop
    columns_to_drop = [
        'DelayCode_Description', 'DelayCodeId', 'SpecialServiceType',
        'SecondPumpArriving_DeployedFromStation', 'SecondPumpArriving_AttendanceTime', 
        'DateAndTimeReturned', 'FRS', 'Notional Cost (£)', 'ResourceMobilisationId', 
        'Resource_Code', 'PerformanceReporting', 'PlusCode_Code', 'PlusCode_Description',
        'CalYear_y', 'HourOfCall_y'
    ]
    cleaned_data.drop(columns=columns_to_drop, inplace=True)

    return cleaned_data

def handle_missing_data(cleaned_data):
    """
    Handle missing values by calculating missing data percentages and filling or dropping missing values.
    
    Params:
        - cleaned_data: DataFrame with cleaned data after removing duplicates.
        
    Returns:
        - cleaned_data: DataFrame with missing data handled.
        - missing_data_summary: DataFrame summarizing missing data and its percentage.
    """
    missing_values_count = cleaned_data.isnull().sum()
    missing_values_percent = (missing_values_count / len(cleaned_data)) * 100
    missing_data_summary = pd.DataFrame({
        'Missing Values': missing_values_count,
        'Percentage': missing_values_percent
    })
    missing_data_summary.sort_values(by='Percentage', ascending=False, inplace=True)

    # Drop rows where certain columns have missing values
    cleaned_data.dropna(subset=['USRN'], inplace=True)

    return cleaned_data, missing_data_summary
