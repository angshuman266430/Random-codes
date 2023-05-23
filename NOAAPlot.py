import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
xls = pd.ExcelFile('NOAA Tide Data Isaac.xlsx')

# Loop over each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = xls.parse(sheet_name)

    # Convert the 'Date' columns to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df.iloc[:,2] = pd.to_datetime(df.iloc[:,2])

    # Plot the time series
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['NOAA'], label='NOAA')
    plt.plot(df.iloc[:,2], df['Original'], label='Original')
    plt.plot(df.iloc[:,2], df['Optimized'], label='Optimized')

    # Set the title and labels
    plt.title(sheet_name)
    plt.xlabel('Date')
    plt.ylabel('Water Surface Elevation (ft)')

    # Rotate x-axis labels to prevent overlap
    plt.xticks(rotation=45)

    # Add a legend
    plt.legend()

    # Save the plot as a PNG file
    plt.savefig(f'{sheet_name}.png', bbox_inches='tight')

    # Close the plot to free up memory
    plt.close()
