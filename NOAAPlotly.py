import pandas as pd
import plotly.graph_objects as go

# Load the Excel file
xls = pd.ExcelFile('NOAA Tide Data Isaac.xlsx')

# Loop over each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = xls.parse(sheet_name)

    # Convert the 'Date' columns to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.iloc[:,2] = pd.to_datetime(df.iloc[:,2])

    # Create a new plot
    fig = go.Figure()

    # Add the time series to the plot
    fig.add_trace(go.Scatter(x=df['Date'], y=df['NOAA'], mode='lines', name='NOAA'))
    fig.add_trace(go.Scatter(x=df.iloc[:,2], y=df['Original'], mode='lines', name='Original'))
    fig.add_trace(go.Scatter(x=df.iloc[:,2], y=df['Optimized'], mode='lines', name='Optimized'))

    # Set the title and labels
    fig.update_layout(title=sheet_name, xaxis_title='Date', yaxis_title='Water Surface Elevation (ft)')

    # Save the plot as an HTML file
    fig.write_html(f'{sheet_name}.html')
