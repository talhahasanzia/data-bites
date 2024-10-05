import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load the dataset from a CSV file
df = pd.read_csv('exchange_rates.csv')

# Convert the Date column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Initialize the plot
fig, ax = plt.subplots(figsize=(14, 6))

# Set up the basic plot elements
ax.set_title('Animated Dollar Exchange Rates Over Time (PKR and INR)', fontsize=16)
ax.set_xlabel('Date', fontsize=14)
ax.set_ylabel('Exchange Rate', fontsize=14)
ax.set_xlim(df['Date'].min(), df['Date'].max())
ax.set_ylim(df[['Dollar in PKR', 'Dollar in INR']].min().min(), df[['Dollar in PKR', 'Dollar in INR']].max().max())

# Create empty line objects for Dollar in PKR and Dollar in INR
line_pk = ax.plot([], [], label='Dollar in PKR', color='green')[0]
line_inr = ax.plot([], [], label='Dollar in INR', color='blue')[0]

# Set up legend
ax.legend()

# Update function for animation
def update(frame):
    current_date = df['Date'].unique()[frame]
    data_until_now = df[df['Date'] <= current_date]
    
    line_pk.set_data(data_until_now['Date'], data_until_now['Dollar in PKR'])
    line_inr.set_data(data_until_now['Date'], data_until_now['Dollar in INR'])
    
    return line_pk, line_inr

# Number of frames in the animation corresponds to the number of unique Date values
num_frames = len(df['Date'].unique())

# Create the animation
ani = FuncAnimation(fig, update, frames=num_frames, repeat=False, interval=200)  # Set interval to control speed

# Display the animation
plt.show()
