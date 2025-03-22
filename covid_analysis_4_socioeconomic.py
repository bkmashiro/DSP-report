#!/usr/bin/env python
# coding: utf-8

#  # COVID-19 Data Analysis: Health and Socioeconomic Impact
#  
#  This notebook analyzes the health and socioeconomic impacts of COVID-19, focusing on the following research questions:
#  1. How COVID-19 affects life expectancy across different regions
#  2. Comparison between health impacts (cases, deaths) and economic impacts (GDP decline, unemployment)
#  3. Whether low-income countries are disproportionately affected compared to wealthy countries

# ## 1. Prep

# In[1]:


# import libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import statsmodels.api as sm
from scipy import stats

# import utils
from covid_analysis_utils import *

# setup fonts not used
# setup_chinese_fonts()

# setup plot style
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12


# In[2]:


# load data
df = load_and_preprocess_data()
print(f"size: {df.shape}")
df.head()


# ## 2. Clean

# In[3]:


df_clean = clean_data(df)


# In[4]:


# Check socioeconomic related columns
socio_columns = ['gdp_per_capita', 'extreme_poverty', 'life_expectancy', 'human_development_index']
print("Socioeconomic related columns:")
for col in socio_columns:
    print(f"- {col}")

# Check data availability
print("\nData availability (non-null percentage):")
for col in socio_columns:
    non_null_pct = (df_clean[col].notnull().sum() / len(df_clean)) * 100
    print(f"- {col}: {non_null_pct:.2f}%")


# In[5]:


plot_frequency_distribution(
    df_clean, [*socio_columns])



# In[6]:


plot_frequency_distribution(
    df_clean, ["total_deaths_per_million"])


# In[7]:


# Filter countries with sufficient socioeconomic data
# Focus on countries with GDP and life expectancy data
country_socio_data = df_clean.groupby('location').agg({
    'gdp_per_capita': 'count',
    'life_expectancy': 'count'
}).reset_index()

# Filter countries that have both GDP and life expectancy data
countries_with_socio_data = country_socio_data[
    (country_socio_data['gdp_per_capita'] > 0) & 
    (country_socio_data['life_expectancy'] > 0)
]['location'].tolist()

print(f"Number of countries with socioeconomic data: {len(countries_with_socio_data)}")

# Filter data for these countries
socio_df = df_clean[df_clean['location'].isin(countries_with_socio_data)].copy()
print(f"Size of filtered data: {socio_df.shape}")


# In[8]:


plot_frequency_distribution(
    socio_df, [*socio_columns])


# In[9]:


plot_frequency_distribution(
    socio_df, ["total_deaths_per_million"])


# ## 3. COVID-19 to life expectancy

# In[10]:


# Analyze relationship between COVID-19 mortality rate and life expectancy

# Calculate cumulative mortality rate (per million) for each country
country_mortality = socio_df.groupby('location').agg({
    'total_deaths_per_million': 'max',  # Use maximum value (latest cumulative)
    'life_expectancy': 'first',  # Use first value (relatively constant)
    'continent': 'first',  # Record continent
    'gdp_per_capita': 'first'  # Record GDP per capita
}).reset_index()

# Remove rows with NaN mortality rate
country_mortality = country_mortality.dropna(subset=['total_deaths_per_million', 'life_expectancy'])

# Group by continent to examine regional differences
continent_mortality = country_mortality.groupby('continent').agg({
    'total_deaths_per_million': 'mean',
    'life_expectancy': 'mean', 
    'location': 'count'  # Count number of countries per continent
}).reset_index()
continent_mortality.columns = ['continent', 'avg_deaths_per_million', 'avg_life_expectancy', 'country_count']

# Sort results
continent_mortality = continent_mortality.sort_values('avg_deaths_per_million', ascending=False)

print("COVID-19 mortality rate and average life expectancy by continent:")
print(continent_mortality)


# In[11]:


plot_frequency_distribution(
    country_mortality, ["total_deaths_per_million", "life_expectancy", "gdp_per_capita"])


# In[12]:


# Create scatter plot: Life Expectancy vs COVID-19 Mortality Rate
plt.figure(figsize=(12, 8))

# Set different colors by continent
continents = country_mortality['continent'].unique()
colors = plt.cm.tab10(np.linspace(0, 1, len(continents)))
continent_color_map = dict(zip(continents, colors))

# Draw scatter plot
for continent in continents:
    if pd.isna(continent):
        continue
    continent_data = country_mortality[country_mortality['continent'] == continent]
    plt.scatter(continent_data['life_expectancy'], 
                continent_data['total_deaths_per_million'],
                label=continent, color=continent_color_map[continent],
                alpha=0.7, s=50)

# Annotate selected countries
for i, row in country_mortality.iterrows():
    if row['total_deaths_per_million'] > 3000 or row['total_deaths_per_million'] < 100 and row['life_expectancy'] > 75:
        plt.annotate(row['location'], 
                     xy=(row['life_expectancy'], row['total_deaths_per_million']),
                     xytext=(5, 0), textcoords='offset points')

plt.xlabel('Life Expectancy (years)')
plt.ylabel('COVID-19 Deaths per Million (cumulative)')
plt.title('Relationship between Life Expectancy and COVID-19 Mortality Rate')
plt.legend(title='Continent')
plt.grid(True, alpha=0.3)
plt.tight_layout()


# In[13]:


# Calculate correlation between life expectancy and mortality rate
corr, p_value = stats.pearsonr(country_mortality['life_expectancy'], country_mortality['total_deaths_per_million'])
print(f"Correlation coefficient between life expectancy and COVID-19 mortality rate: {corr:.3f} (p={p_value:.3f})")

# Perform simple linear regression
X = sm.add_constant(country_mortality['life_expectancy'])
model = sm.OLS(country_mortality['total_deaths_per_million'], X).fit()
print(model.summary())


# In[14]:


# Estimate life expectancy loss due to COVID-19
# Based on WHO data, age-adjusted mortality rate can be used to estimate changes in life expectancy
# Here we use a simplified method: assume every 1000 deaths per million population leads to about 0.1 year decrease in life expectancy

country_mortality['estimated_life_expectancy_loss'] = country_mortality['total_deaths_per_million'] / 1000 * 0.1

# View top 10 countries with highest life expectancy loss
top_life_expectancy_loss = country_mortality.sort_values('estimated_life_expectancy_loss', ascending=False).head(10)
print("Top 10 countries with highest estimated life expectancy loss:")
print(top_life_expectancy_loss[['location', 'total_deaths_per_million', 'estimated_life_expectancy_loss', 'life_expectancy']])

# Group by continent
continent_life_loss = country_mortality.groupby('continent').agg({
    'estimated_life_expectancy_loss': 'mean'
}).reset_index()

print("\nEstimated average life expectancy loss by continent:")
print(continent_life_loss.sort_values('estimated_life_expectancy_loss', ascending=False))


# ## 4. Health Impact vs Economic Impact

# In[15]:


# Load World Bank GDP data
def load_worldbank_data():
    """Load and process World Bank GDP data"""
    # Read GDP indicator data
    gdp_growth = pd.read_csv('worldbank/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_76269.csv', skiprows=4)
    gdp_per_capita = pd.read_csv('worldbank/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_76317.csv', skiprows=4)
    gdp_per_capita_growth = pd.read_csv('worldbank/API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_76067.csv', skiprows=4)
    gdp_current = pd.read_csv('worldbank/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_76261.csv', skiprows=4)
    
    # Select required columns
    columns = ['Country Code', 'Country Name', '2019', '2020', '2021', '2022']
    
    # Rename dataframes
    gdp_growth = gdp_growth[columns].rename(columns={'2019': 'gdp_growth_2019', '2020': 'gdp_growth_2020', 
                                                    '2021': 'gdp_growth_2021', '2022': 'gdp_growth_2022'})
    gdp_per_capita = gdp_per_capita[columns].rename(columns={'2019': 'gdp_per_capita_2019', '2020': 'gdp_per_capita_2020',
                                                            '2021': 'gdp_per_capita_2021', '2022': 'gdp_per_capita_2022'})
    gdp_per_capita_growth = gdp_per_capita_growth[columns].rename(columns={'2019': 'gdp_per_capita_growth_2019',
                                                                         '2020': 'gdp_per_capita_growth_2020',
                                                                         '2021': 'gdp_per_capita_growth_2021',
                                                                         '2022': 'gdp_per_capita_growth_2022'})
    gdp_current = gdp_current[columns].rename(columns={'2019': 'gdp_current_2019', '2020': 'gdp_current_2020',
                                                     '2021': 'gdp_current_2021', '2022': 'gdp_current_2022'})
    
    # Merge all data
    gdp_data = pd.merge(gdp_growth, gdp_per_capita, on=['Country Code', 'Country Name'])
    gdp_data = pd.merge(gdp_data, gdp_per_capita_growth, on=['Country Code', 'Country Name'])
    gdp_data = pd.merge(gdp_data, gdp_current, on=['Country Code', 'Country Name'])
    
    # Calculate GDP changes (using GDP growth data instead of current GDP)
    gdp_data['gdp_change_2020'] = gdp_data['gdp_growth_2020']
    gdp_data['gdp_change_2021'] = gdp_data['gdp_growth_2021'] 
    gdp_data['gdp_change_2022'] = gdp_data['gdp_growth_2022']
    
    return gdp_data


# In[16]:


# load additional data: GDP data
gdp_data = load_worldbank_data()


# In[17]:


gdp_data.head()


# In[18]:


country_impact = socio_df.groupby('location').agg({
    'stringency_index': 'mean',
    'total_deaths_per_million': 'max', 
    'gdp_per_capita': 'first',
    'continent': 'first'
}).reset_index()
print(country_impact.shape)
country_impact.head()


# In[19]:


# Since we don't have direct GDP decline data, we'll use the stringency index as a proxy for economic impact
# Generally, strict restriction measures lead to greater economic losses in the short term

# Calculate average stringency index and death rate for each country

country_impact = pd.merge(
    country_impact,
    gdp_data,
    left_on='location',
    right_on='Country Name'
)

# Remove rows with missing values
country_impact = country_impact.dropna(subset=['stringency_index', 'total_deaths_per_million', 'gdp_per_capita'])

# Group countries into high/medium/low by GDP
country_impact['gdp_group'] = pd.qcut(country_impact['gdp_per_capita'], 3, labels=['Low Income', 'Middle Income', 'High Income'])
country_impact['income_level'] = pd.qcut(country_impact['gdp_per_capita'], 
                                       q=4, 
                                       labels=['Low', 'Medium-Low', 'Medium-High', 'High'])


# In[20]:


# drop all unmatched pairs

print(country_impact.shape)
country_impact


# In[21]:


print("\nGDP Impact Analysis:")
print("\n1. Correlation between Stringency Index and GDP Change:")
corr, p_value = stats.pearsonr(country_impact['stringency_index'], country_impact['gdp_change_2020'])
print(f"Correlation: {corr:.3f} (p={p_value:.3f})")

print("\n2. GDP Changes by Continent:")
continent_gdp = country_impact.groupby('continent').agg({
    'gdp_change_2020': ['mean', 'std', 'count'],
    'gdp_change_2021': ['mean', 'std'],
    'gdp_change_2022': ['mean', 'std'],
    'stringency_index': 'mean'
}).round(2)
print(continent_gdp)


# In[22]:


plt.figure(figsize=(10, 6))
sns.scatterplot(data=country_impact, x='stringency_index', y='gdp_change_2020', hue='continent')
plt.title('Stringency Index vs GDP Change (2020)')
plt.xlabel('Average Stringency Index')
plt.ylabel('GDP Change (%)')
plt.legend(title='Continent')
plt.tight_layout()
plt.savefig('ca/images/gdp_stringency_relation.png')


# In[23]:


plt.figure(figsize=(10, 6))
sns.boxplot(data=country_impact, x='continent', y='gdp_change_2020')
plt.title('GDP Change Distribution by Continent (2020)')
plt.xlabel('Continent')
plt.ylabel('GDP Change (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ca/images/gdp_continent_boxplot.png')


# In[24]:


plt.figure(figsize=(12, 6))
continent_trend = country_impact.groupby('continent')[['gdp_change_2020', 'gdp_change_2021', 'gdp_change_2022']].mean()
continent_trend.plot(kind='bar')
plt.title('GDP Change Trend by Continent')
plt.xlabel('Continent')
plt.ylabel('GDP Change (%)')
plt.legend(title='Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ca/images/gdp_trend_by_continent.png')


# In[25]:


plt.figure(figsize=(10, 6))
sns.scatterplot(data=country_impact, x='gdp_per_capita_2019', y='gdp_change_2020', hue='continent')
plt.title('GDP per Capita vs GDP Change (2020)')
plt.xlabel('GDP per Capita (2019)')
plt.ylabel('GDP Change (%)')
plt.legend(title='Continent')
plt.tight_layout()
plt.savefig('ca/images/gdp_per_capita_relation.png')


# In[26]:


plt.figure(figsize=(10, 6))
sns.boxplot(data=country_impact, x='income_level', y='gdp_change_2020')
plt.title('GDP Change by Income Level (2020)')
plt.xlabel('Income Level')
plt.ylabel('GDP Change (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('ca/images/gdp_income_level.png')


# In[27]:


plt.figure(figsize=(12, 6))

# Plot scatter points
sns.scatterplot(data=country_impact, x='stringency_index', y='gdp_change_2020', 
                hue='income_level', alpha=0.5)

# Add regression lines for each income level
for income in country_impact['income_level'].unique():
    income_data = country_impact[country_impact['income_level'] == income]
    sns.regplot(data=income_data, x='stringency_index', y='gdp_change_2020',
                scatter=False, label=f'{income} (trend)')

plt.title('Stringency Index vs GDP Change by Income Level with Trend Lines (2020)')
plt.xlabel('Average Stringency Index')
plt.ylabel('GDP Change (%)')
plt.legend(title='Income Level')
plt.tight_layout()
plt.savefig('ca/images/gdp_stringency_income.png')


# In[28]:


# Analyze stringency index and mortality rate by GDP group and continent
# Calculate averages by GDP group
gdp_group_impact = country_impact.groupby('gdp_group').agg({
    'stringency_index': 'mean',
    'total_deaths_per_million': 'mean', 
    'gdp_per_capita': 'mean',
    'location': 'count'
}).reset_index()

print("Health and economic impacts by income level:")
print(gdp_group_impact)

# Calculate averages by continent
continent_impact = country_impact.groupby('continent').agg({
    'stringency_index': 'mean',
    'total_deaths_per_million': 'mean',
    'gdp_per_capita': 'mean', 
    'location': 'count'
}).reset_index()

print("\nHealth and economic impacts by continent:")
print(continent_impact)


# In[29]:


# Compare stringency-mortality efficiency across GDP groups
# Calculate efficiency ratio for each country: mortality rate / stringency index
# Lower ratio indicates lower mortality per unit of stringency, i.e. higher policy efficiency
# Filter out data with stringency index of 0 to avoid division by zero
country_impact_filtered = country_impact[country_impact['stringency_index'] > 0]
country_impact_filtered['efficiency_ratio'] = country_impact_filtered['total_deaths_per_million'] / country_impact_filtered['stringency_index']

# Calculate average efficiency ratios by GDP group
gdp_efficiency = country_impact_filtered.groupby('gdp_group').agg({
    'efficiency_ratio': ['mean', 'median', 'std'],
    'location': 'count'
}).reset_index()

print("Policy efficiency by income level:")
print(gdp_efficiency)


# In[30]:


# Create boxplot: efficiency ratio by GDP group
plt.figure(figsize=(12, 7))
sns.boxplot(x='gdp_group', y='efficiency_ratio', data=country_impact_filtered, palette='viridis')
plt.xlabel('Income Level Group')
plt.ylabel('Efficiency Ratio (Deaths/Stringency)')
plt.title('Policy Efficiency Comparison Across Income Levels')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('ca/images/efficiency-gdp.png')


# ## 5. Low income countries disproportionate impact

# In[31]:


# Analyze relationship between extreme poverty and COVID-19 impact
# Check availability of extreme poverty data
poverty_data_count = socio_df['extreme_poverty'].notnull().sum()
print(f"Extreme poverty data availability: {poverty_data_count} rows ({poverty_data_count/len(socio_df)*100:.2f}%)")

# Calculate extreme poverty rate and COVID-19 impact for each country
country_poverty = socio_df.groupby('location').agg({
    'extreme_poverty': 'first',
    'total_deaths_per_million': 'max',
    'gdp_per_capita': 'first',
    'continent': 'first',
    'stringency_index': 'mean'
}).reset_index()

# Remove rows with NaN extreme poverty rate
country_poverty = country_poverty.dropna(subset=['extreme_poverty', 'total_deaths_per_million'])
print(f"Number of countries with extreme poverty data: {len(country_poverty)}")


# In[32]:


# Create scatter plot: Extreme poverty rate vs COVID-19 deaths
plt.figure(figsize=(12, 8))

# Create scatter plot
plt.scatter(country_poverty['extreme_poverty'], 
            country_poverty['total_deaths_per_million'],
            alpha=0.7, s=50, c=country_poverty['gdp_per_capita'], cmap='viridis')

# Add colorbar
plt.colorbar(label='GDP per capita (USD)')

# Label selected countries
# for i, row in country_poverty.iterrows():
#     if row['extreme_poverty'] > 40 or row['total_deaths_per_million'] > 5000:
#         plt.annotate(row['location'], 
#                      xy=(row['extreme_poverty'], row['total_deaths_per_million']),
#                      xytext=(5, 0), textcoords='offset points')

plt.xlabel('Extreme Poverty Rate (%)')
plt.ylabel('COVID-19 Deaths per Million')
plt.title('Relationship between Extreme Poverty and COVID-19 Mortality')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ca/images/proverty-death.png')


# In[33]:


# Calculate correlation between extreme poverty rate and mortality rate
corr, p_value = stats.pearsonr(country_poverty['extreme_poverty'], country_poverty['total_deaths_per_million'])
print(f"Correlation coefficient between extreme poverty rate and COVID-19 mortality rate: {corr:.3f} (p={p_value:.3f})")

# Plot regression line
plt.figure(figsize=(12, 8))
sns.regplot(x='extreme_poverty', y='total_deaths_per_million', data=country_poverty, scatter_kws={'alpha':0.7})
plt.xlabel('Extreme Poverty Rate (%)')
plt.ylabel('COVID-19 Deaths per Million')
plt.title('Correlation between Extreme Poverty and COVID-19 Mortality Rate')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ca/images/poverty_mortality_correlation.png')


# In[34]:


# Multiple regression analysis: Impact of GDP, extreme poverty and stringency on mortality rate
# First remove rows with missing values
country_poverty_clean = country_poverty.dropna(subset=['gdp_per_capita', 'extreme_poverty', 'stringency_index', 'total_deaths_per_million'])

X = country_poverty_clean[['gdp_per_capita', 'extreme_poverty', 'stringency_index']]
X = sm.add_constant(X)  # Add constant term
y = country_poverty_clean['total_deaths_per_million']

# Fit model
model = sm.OLS(y, X).fit()
print(model.summary())


# In[35]:


# Analyze extreme poverty and COVID-19 impact by income level
# Group countries by GDP
country_poverty['gdp_group'] = pd.qcut(country_poverty['gdp_per_capita'], 3, labels=['Low Income', 'Middle Income', 'High Income'])

# Analyze by GDP group and poverty level
# Split extreme poverty rate into three groups: low (<5%), medium (5-20%), high (>20%)
country_poverty['poverty_group'] = pd.cut(country_poverty['extreme_poverty'],
                                        bins=[0, 5, 20, 100],
                                        labels=['Low Poverty', 'Medium Poverty', 'High Poverty'])

# Calculate average mortality rate for each GDP and poverty combination
poverty_gdp_impact = country_poverty.groupby(['gdp_group', 'poverty_group']).agg({
    'total_deaths_per_million': ['mean', 'count'],
    'stringency_index': 'mean'
}).reset_index()

print("COVID-19 mortality rates by income and poverty level:")
print(poverty_gdp_impact)


# In[36]:


# Create heatmap: GDP groups x Poverty groups vs Mortality rate
# Reshape data into format suitable for heatmap
heatmap_data = poverty_gdp_impact.pivot_table(
    index='gdp_group', 
    columns='poverty_group', 
    values=['total_deaths_per_million'],
    aggfunc='mean'
)

plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd')
plt.title('COVID-19 Mortality Rate by Income and Poverty Level')
plt.tight_layout()
plt.savefig("ca/images/proverty-death-heatmap.png")


# # 6. Conclusions and Findings
# 
# Through our analysis of COVID-19's health and socioeconomic impacts, we have reached the following key findings:
# 
# 1. **Impact on Life Expectancy**: COVID-19 has had a significant negative impact on global life expectancy, particularly in regions with high mortality rates such as South America and Europe. According to our estimates, life expectancy may have declined by 0.3-0.7 years in the most severely affected countries. While this decline may seem small, it's worth noting that historically, even small improvements in life expectancy have required years of public health efforts.
# 
# 2. **Relationship Between Health and Economic Impacts**: The data reveals a complex relationship between health impacts (mortality rates) and economic impacts (restrictive measures represented by the stringency index). Generally, high-income countries achieved lower mortality rates under similar stringency levels, indicating higher policy efficiency, likely due to stronger healthcare systems and better social security.
# 
# 3. **Disproportionate Impact on Low-Income Countries**: While low-income countries with high extreme poverty rates don't necessarily show higher official COVID-19 mortality rates (possibly due to limited testing and reporting capabilities), multivariate regression analysis indicates that poverty is indeed associated with adverse health outcomes when controlling for other factors. Notably, middle-income countries with high poverty rates often showed the worst health outcomes, suggesting they face dual challenges of healthcare system pressure and socioeconomic vulnerabilities.
# 
# 4. **Regional Differences**: The impact varies significantly across regions. Europe and South America generally showed higher mortality rates, while Asia and Oceania performed relatively better. This may reflect the influence of various factors including cultural elements, social structures, prior epidemic experience, and the timeliness and appropriateness of response measures.
# 
# Overall, these findings emphasize that COVID-19 is not just a health crisis but also a profound socioeconomic crisis, with impacts unevenly distributed across countries and population groups. This understanding is crucial for developing more inclusive and targeted public health policies, as well as preparing for potential future pandemics.
