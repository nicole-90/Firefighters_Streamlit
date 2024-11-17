# Firefighters_Streamlit_Functions_part2.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_incidents_by_year(LFB_viz):
    """Plots the number of incidents by year."""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=LFB_viz, x='Year', palette='viridis')
    plt.title('Number of Incidents by Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45)
    return plt

def plot_incidents_by_day(LFB_viz):
    """Plots the number of incidents by day of the week."""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=LFB_viz, x='DayOfWeek', order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], palette='viridis')
    plt.title('Number of Incidents by Day of the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45)
    return plt

def plot_incidents_by_hour(LFB_viz):
    """Plots the number of incidents by hour of the day."""
    plt.figure(figsize=(10, 6))
    sns.countplot(data=LFB_viz, x='HourOfCall', palette='viridis')
    plt.title('Number of Incidents by Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45)
    return plt

def plot_incidents_by_type(LFB_viz):
    """Plots the number of incidents by incident type."""
    plt.figure(figsize=(12, 6))
    sns.countplot(data=LFB_viz, x='IncidentType', order=LFB_viz['IncidentType'].value_counts().index, palette='viridis')
    plt.title('Number of Incidents by Incident Type')
    plt.xlabel('Incident Type')
    plt.ylabel('Number of Incidents')
    plt.xticks(rotation=45)
    return plt

def plot_incidents_by_area(LFB_viz):
    """Plots the number of incidents by London Area."""
    plt.figure(figsize=(10, 6))
    sns.countplot(x='LondonArea', data=LFB_viz, palette='viridis')
    plt.title('Number of Incidents by London Area')
    plt.xlabel('London Area')
    plt.ylabel('Number of Incidents')
    return plt

def plot_attendance_time(LFB_viz):
    """Plots average attendance time by London Area."""
    plt.figure(figsize=(10, 6))
    sns.barplot(data=LFB_viz, x='LondonArea', y='AttendanceTimeMinutes', palette='viridis', ci=None)
    plt.title('Average Attendance Time by London Area')
    plt.xlabel('London Area')
    plt.ylabel('Average Attendance Time (Minutes)')
    return plt

def plot_correlation_heatmap(LFB_viz):
    """Plots the correlation heatmap."""
    correlation_columns = [
        'TurnoutTimeSecs', 'TravelTimeSecs', 'AttendanceTimeMinutes', 
        'PumpMinutesUsed', 'FirstPumpArrivalTime', 'NumStationsAttending', 
        'NumPumpsAttending', 'PumpOrder', 'HourOfCall', 'Easting_rounded', 'Northing_rounded'
    ]
    correlation_matrix = LFB_viz[correlation_columns].corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Expanded Correlation Heatmap of Response Times and Resources Used')
    return plt
