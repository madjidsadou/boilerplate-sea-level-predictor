import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np

def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create first line of best fit for all years
    slope, intercept, r_value, p_value, std_err = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    
    # Generate predicted values for the available data (existing years)
    y_pred = slope * df['Year'] + intercept
    
    # Generate predicted values for future years (from the maximum year in data to 2050)
    future_years = np.arange(df['Year'].max(), 2051)  # Years from the max year in data to 2050
    future_y_pred = slope * future_years + intercept  # Extrapolated predictions
    
    # Create a new DataFrame for the available data and predicted data (combining them)
    df_combined = df.copy()
    future_df = pd.DataFrame({
        'Year': future_years,
        'CSIRO Adjusted Sea Level': future_y_pred
    })
    
    # Append the future DataFrame to the original DataFrame
    df_combined = pd.concat([df_combined, future_df], ignore_index=True)

    # Create scatter plot for the available data
    plt.scatter(df['Year'], df['CSIRO Adjusted Sea Level'], label='Data (All Years)', color='blue')

    # Plot the line of best fit for the available data
    plt.plot(df['Year'], y_pred, label=f'Fit Line (slope={slope:.2f})', color='red')

    # Plot the extrapolated line for future years (from max year to 2050)
    plt.plot(future_years, future_y_pred, label='Extrapolated Fit Line (All Years)', color='green', linestyle='--')

    # Filter data for years >= 2000
    new = df[df['Year'] >= 2000]
    
    # Create second line of best fit for years >= 2000
    slope2, intercept2, r_value2, p_value2, std_err2 = linregress(new['Year'], new['CSIRO Adjusted Sea Level'])
    y_pred2000 = slope2 * new['Year'] + intercept2

    # Generate predicted values for future years (from max year to 2050)
    future_y_pred2000 = slope2 * future_years + intercept2  # Extrapolated predictions for 2000+ years

    # Create DataFrame for the second line's future predictions
    future_df2 = pd.DataFrame({
        'Year': future_years,
        'CSIRO Adjusted Sea Level': future_y_pred2000
    })
    
    # Append the second line's predicted data to the combined DataFrame for years >= 2000
    df_combined2 = pd.concat([new, future_df2], ignore_index=True)
    print(new.shape)
    # Plot the line of best fit for years >= 2000
    plt.plot(new['Year'], y_pred2000, label=f'Fit Line (2000 and later, slope={slope2:.2f})', color='purple')

    # Plot the extrapolated line for future years (2010 to 2050) based on the 2000+ data
    plt.plot(future_years, future_y_pred2000, label='Extrapolated Fit Line (2000 and later)', color='orange', linestyle='--')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')


    # Display the plot
    plt.show()

    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()
