import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick # For percentage formatting
import matplotlib.colors as mcolors # For color manipulation
import io

# Your provided data
data_string = """
2015	Active	237	2825	0.08
2015	Churned	2588	2825	0.92
2016	Active	311	3397	0.09
2016	Churned	3086	3397	0.91
2017	Active	385	4068	0.09
2017	Churned	3683	4068	0.91
2018	Active	704	7446	0.09
2018	Churned	6742	7446	0.91
2019	Active	687	7755	0.09
2019	Churned	7068	7755	0.91
2020	Active	283	3031	0.09
2020	Churned	2748	3031	0.91
2021	Active	442	4663	0.09
2021	Churned	4221	4663	0.91
2022	Active	937	9010	0.10
2022	Churned	8073	9010	0.90
2023	Active	455	4718	0.10
2023	Churned	4263	4718	0.90
"""

# Read the data into a DataFrame
df = pd.read_csv(io.StringIO(data_string), sep='\t', header=None,
                 names=['cohort_year', 'customer_status', 'num_customers', 'total_customers', 'status_percentage'])

# Define the blue color scheme
# A nice, standard blue for 'Active'
active_color = 'royalblue' # Solid blue
# Same blue for 'Churned', but with transparency (alpha channel)
# "more opaque see through blue" -> alpha around 0.6-0.7 should work
churned_color_transparent = mcolors.to_rgba('royalblue', alpha=0.65)

colors_for_plot = [active_color, churned_color_transparent]

# --- Visualization 1: Stacked Bar Chart with Counts ---

# Pivot the data to get 'Active' and 'Churned' counts as columns for each year
pivot_counts_df = df.pivot_table(index='cohort_year',
                                 columns='customer_status',
                                 values='num_customers').fillna(0)

# Ensure the columns are in a consistent order for color mapping: Active then Churned
pivot_counts_df = pivot_counts_df[['Active', 'Churned']]

fig1, ax1 = plt.subplots(figsize=(12, 7))

# Plotting with the new blue color scheme
pivot_counts_df.plot(kind='bar', stacked=True, ax=ax1, color=colors_for_plot)

ax1.set_title('Customer Status by Cohort Year (Counts)', fontsize=16)
ax1.set_xlabel('Cohort Year', fontsize=12)
ax1.set_ylabel('Number of Customers', fontsize=12)
ax1.tick_params(axis='x', rotation=45)
ax1.legend(title='Customer Status')
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# Add text annotations for counts
# Using a loop to handle colors for text if needed, but white should still be fine
for i, container_group in enumerate(ax1.containers):
    # For 'Active' (index 0, solid blue), white text is good.
    # For 'Churned' (index 1, transparent blue), white text should also be good.
    # If churned color was very light, might need black text.
    text_color = 'white'
    ax1.bar_label(container_group, label_type='center', fmt='%d', color=text_color, weight='bold', fontsize=9)

plt.tight_layout()
plt.show()


# --- Visualization 2: Stacked Bar Chart with Percentages ---

# Pivot the data to get 'Active' and 'Churned' percentages as columns for each year
pivot_perc_df = df.pivot_table(index='cohort_year',
                               columns='customer_status',
                               values='status_percentage').fillna(0)

# Ensure the columns are in a consistent order: Active then Churned
pivot_perc_df = pivot_perc_df[['Active', 'Churned']]


fig2, ax2 = plt.subplots(figsize=(12, 7))

# Plotting with the new blue color scheme
pivot_perc_df.plot(kind='bar', stacked=True, ax=ax2, color=colors_for_plot)

ax2.set_title('Customer Status by Cohort Year (Percentage)', fontsize=16)
ax2.set_xlabel('Cohort Year', fontsize=12)
ax2.set_ylabel('Percentage of Customers', fontsize=12)
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0)) # Format y-axis as percentage
ax2.tick_params(axis='x', rotation=45)
ax2.legend(title='Customer Status')
ax2.grid(axis='y', linestyle='--', alpha=0.7)

# Add text annotations for percentages
# Iterate through years and statuses to place text
# Keep track of the bottom of the current bar segment for text placement
current_bottom_heights = [0.0] * len(pivot_perc_df.index)

for i, status_col in enumerate(pivot_perc_df.columns): # 'Active', then 'Churned'
    text_color = 'white' # White text for both
    for bar_idx, (year_idx, value) in enumerate(pivot_perc_df[status_col].items()):
        if value > 0.01: # Only add text if the segment is somewhat visible
            # Calculate the vertical center of the bar segment
            bar_center_y = current_bottom_heights[bar_idx] + value / 2
            ax2.text(bar_idx, bar_center_y, f"{value*100:.0f}%",
                     ha='center', va='center', color=text_color, weight='bold', fontsize=9)
    # Update the bottom height for the next stack in the next status column
    current_bottom_heights = [b + h for b, h in zip(current_bottom_heights, pivot_perc_df[status_col])]


plt.tight_layout()
plt.show()