import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the dataset from a CSV file
df = pd.read_csv('rankings.csv')

# Convert the rank_date column to datetime format
df['rank_date'] = pd.to_datetime(df['rank_date'])

# Group by country and filter out those who were ever ranked greater than 25
countries_never_below_25 = df.groupby('country_full').filter(lambda x: x['rank'].max() <= 25)['country_full'].unique()

# Filter the dataset to only include these countries
filtered_df = df[df['country_full'].isin(countries_never_below_25)]

# Sort by rank_date
filtered_df = filtered_df.sort_values(by='rank_date')

# Initialize the plot
fig, ax = plt.subplots(figsize=(16, 8))

# Set up the basic plot elements
ax.set_title('Animated Rank Trend of Countries Never Below Rank 25', fontsize=16)
ax.set_xlabel('Year', fontsize=14)
ax.set_ylabel('Rank', fontsize=14)

# Customize the y-axis
max_rank = 25  # Maximum rank value you want to display
ax.set_ylim(max_rank, 0)  # Flip the y-axis with 0 on top and max rank at the bottom
ax.set_yticks(range(0, max_rank + 1))  # Show ranks from 1 to max_rank

# Create a color palette for the countries
palette = sns.color_palette("hsv", len(countries_never_below_25))

# Define a dictionary to store the line objects for each country
lines = {country: ax.plot([], [], label=country, color=palette[i])[0] for i, country in enumerate(countries_never_below_25)}

# Set up legend
ax.legend()

# Update function for animation
def update(frame):
    current_date = filtered_df['rank_date'].unique()[frame]
    data_until_now = filtered_df[filtered_df['rank_date'] <= current_date]
    
    for country, line in lines.items():
        country_data = data_until_now[data_until_now['country_full'] == country]
        line.set_data(country_data['rank_date'], country_data['rank'])
    
    ax.set_xlim(filtered_df['rank_date'].min(), filtered_df['rank_date'].max())
    return lines.values()

# Number of frames in the animation corresponds to the number of unique rank_date values
num_frames = len(filtered_df['rank_date'].unique())

# Create the animation and make it smoother by increasing frames and reducing interval
ani = FuncAnimation(fig, update, frames=num_frames, repeat=False, interval=16)  # Set interval to 100ms for smoother animation

# Display the animation
plt.show()
