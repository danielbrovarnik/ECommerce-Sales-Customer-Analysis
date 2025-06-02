import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Load the data (same as before)
data = """
2018	AU	1497129.3626000015
2016	AU	493712.9862
2021	AU	1430683.788999999
2024	AU	546245.6439999989
2023	AU	2210459.2979999855
2019	AU	1721999.3444000017
2015	AU	480825.2054999999
2022	AU	2890173.818500011
2017	AU	639037.3788999994
2020	AU	595489.2999999995
2016	CA	1159264.1618
2019	CA	3362870.1321999985
2024	CA	1063106.8099999975
2021	CA	2334459.1414000015
2023	CA	3921228.6200000336
2020	CA	1184199.4118
2022	CA	4697528.723500081
2017	CA	1424148.3034000008
2015	CA	807509.4325000009
2018	CA	2572768.5571999988
2017	DE	1315342.7763999994
2020	DE	1307678.2543000008
2022	DE	4931508.491200072
2018	DE	2401552.1213999977
2021	DE	2179570.1726999967
2016	DE	1028230.7270000004
2023	DE	4617386.716000053
2019	DE	3283178.5519999973
2015	DE	704993.8925000001
2024	DE	1224638.1599999936
2024	FR	299834.4500000002
2020	FR	360817.5930000002
2023	FR	1275195.105999993
2015	FR	282565.51649999997
2017	FR	358728.94539999985
2021	FR	675950.8295000001
2016	FR	248182.7421000001
2022	FR	1630938.582499991
2019	FR	898870.3585999993
2018	FR	715552.4559999997
2022	GB	3942789.2717000446
2017	GB	1852620.5114000016
2024	GB	735839.349999999
2019	GB	3965509.7133999895
2021	GB	2002125.2324999946
2023	GB	2739848.72
2016	GB	1862566.7379999994
2015	GB	1287734.4271000011
2018	GB	3440355.7713999995
2020	GB	1169367.0542999983
2016	IT	571310.0474999995
2018	IT	1016277.6139999995
2017	IT	802234.9820000001
2019	IT	1130952.8181999999
2020	IT	314336.61599999986
2024	IT	185615.54999999996
2023	IT	828997.359999998
2022	IT	773307.0714999989
2015	IT	332266.21099999984
2021	IT	435951.9719999999
2019	NL	1007062.8007999999
2018	NL	856199.3364000004
2017	NL	404642.77529999963
2020	NL	474698.85990000033
2015	NL	281905.535
2016	NL	389811.59
2021	NL	796041.2400000002
2023	NL	1919262.4799999837
2022	NL	2059007.8199999866
2024	NL	522269.4099999996
2015	US	3885990.9163999986
2017	US	7400828.775499989
2023	US	16390257.430001011
2020	US	6384418.114200026
2019	US	18157394.58580028
2016	US	5421867.725999998
2022	US	25257327.487999268
2021	US	12892330.975999959
2024	US	4026554.7880000467
2018	US	13983880.8242002
"""

df = pd.read_csv(StringIO(data), sep='\t', header=None, names=['Year', 'Country', 'Revenue'])
df['Year'] = df['Year'].astype(int)

# --- Step 1: Determine the country order from the "Average Annual Revenue" pie chart ---
# Filter data for 2015-2023 for average calculation
df_filtered_avg = df[df['Year'] <= 2023]
# Calculate annual percentage contribution
pivot_df_revenue_avg = df_filtered_avg.pivot_table(index='Year', columns='Country', values='Revenue', fill_value=0)
pivot_df_percent_annual_avg = pivot_df_revenue_avg.apply(lambda x: x / x.sum() * 100, axis=1)
# Calculate average annual percentage for each country
average_annual_percentage_avg = pivot_df_percent_annual_avg.mean()
# THIS IS THE CRUCIAL ORDER for the colors, as used in the previous "average" pie chart
ordered_countries_for_color = average_annual_percentage_avg.sort_values(ascending=False).index.tolist()
# print("Order of countries for consistent color mapping (from average pie):", ordered_countries_for_color)

# --- Step 2 & 3: Generate color palette and create the country_color_map based on this order ---
palette = plt.cm.get_cmap('Spectral', len(ordered_countries_for_color))
country_color_map = {country: palette(i) for i, country in enumerate(ordered_countries_for_color)}
# Add any countries present in the full dataset but maybe not in the top avg (though unlikely for this dataset)
# This ensures all countries get a color, even if they had 0 average contribution.
all_unique_countries = df['Country'].unique()
for country in all_unique_countries:
    if country not in country_color_map:
        # Assign a new color from the end of the palette or a default one
        # For simplicity, let's assume 'Spectral' has enough, or re-use.
        # A more robust solution would be to extend the palette if needed.
        # Given the legend image, all relevant countries are in ordered_countries_for_color.
        pass


def create_pie_chart_for_year(dataframe, target_year, color_map_to_use):
    """Helper function to create a pie chart for a specific year with consistent colors."""
    df_year = dataframe[dataframe['Year'] == target_year]

    if df_year.empty:
        print(f"No data found for the year {target_year}.")
        return

    revenue_by_country = df_year.groupby('Country')['Revenue'].sum().sort_values(ascending=False)

    # Prepare colors for the current year's data based on the predefined map
    # Handle cases where a country in a specific year might not be in the original color map
    # (though unlikely here as color map is based on all countries from the average chart)
    year_specific_colors = []
    for country in revenue_by_country.index:
        year_specific_colors.append(color_map_to_use.get(country, '#CCCCCC')) # Default to gray if not found

    explode = [0] * len(revenue_by_country)
    if not revenue_by_country.empty:
        explode[0] = 0.05

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        revenue_by_country,
        autopct='%1.1f%%',
        startangle=140,
        colors=year_specific_colors,
        explode=explode,
        pctdistance=0.80,
        wedgeprops={'edgecolor': 'white', 'linewidth': 0.5}
    )

    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(9)

    ax.set_title(f'Revenue Contribution by Country - {target_year}', fontsize=16, pad=20)
    ax.axis('equal')

    ax.legend(
        wedges,
        revenue_by_country.index,
        title="Countries",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1),
        fontsize=10,
        title_fontsize=12
    )

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.show()

    print(f"\nRevenue Contribution for {target_year}:")
    total_revenue_year = revenue_by_country.sum()
    for country, rev in revenue_by_country.items():
        percentage = (rev / total_revenue_year) * 100 if total_revenue_year > 0 else 0
        print(f"{country}: {rev:,.2f} ({percentage:.2f}%)")

# --- Create Pie Chart for 2015 using the derived color map ---
create_pie_chart_for_year(df, 2015, country_color_map)

# --- Create Pie Chart for 2023 using the derived color map ---
create_pie_chart_for_year(df, 2023, country_color_map)