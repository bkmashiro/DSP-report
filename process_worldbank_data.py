import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def load_worldbank_data():
    """Load and process World Bank GDP data"""
    # 读取各个GDP指标数据
    gdp_growth = pd.read_csv('worldbank/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2_76269.csv', skiprows=4)
    gdp_per_capita = pd.read_csv('worldbank/API_NY.GDP.PCAP.CD_DS2_en_csv_v2_76317.csv', skiprows=4)
    gdp_per_capita_growth = pd.read_csv('worldbank/API_NY.GDP.PCAP.KD.ZG_DS2_en_csv_v2_76067.csv', skiprows=4)
    gdp_current = pd.read_csv('worldbank/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_76261.csv', skiprows=4)
    
    # 选择需要的列
    columns = ['Country Code', 'Country Name', '2019', '2020', '2021', '2022']
    
    # 重命名数据框
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
    
    # 合并所有数据
    gdp_data = pd.merge(gdp_growth, gdp_per_capita, on=['Country Code', 'Country Name'])
    gdp_data = pd.merge(gdp_data, gdp_per_capita_growth, on=['Country Code', 'Country Name'])
    gdp_data = pd.merge(gdp_data, gdp_current, on=['Country Code', 'Country Name'])
    
    # 计算GDP变化
    gdp_data['gdp_change_2020'] = (gdp_data['gdp_current_2020'] - gdp_data['gdp_current_2019']) / gdp_data['gdp_current_2019'] * 100
    gdp_data['gdp_change_2021'] = (gdp_data['gdp_current_2021'] - gdp_data['gdp_current_2019']) / gdp_data['gdp_current_2019'] * 100
    gdp_data['gdp_change_2022'] = (gdp_data['gdp_current_2022'] - gdp_data['gdp_current_2019']) / gdp_data['gdp_current_2019'] * 100
    
    return gdp_data

def analyze_gdp_impact(gdp_data, country_impact):
    """Analyze GDP impact and create visualizations"""
    # 合并数据
    merged_data = pd.merge(
        country_impact,
        gdp_data,
        left_on='iso_code',
        right_on='Country Code'
    )
    
    # 创建GDP影响分析图
    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=merged_data, x='stringency_index', y='gdp_change_2020', hue='continent')
    plt.title('Relationship between Stringency Index and GDP Change in 2020')
    plt.xlabel('Average Stringency Index')
    plt.ylabel('GDP Change (%)')
    plt.savefig('images/gdp_impact.png')
    plt.close()
    
    # 计算相关系数
    corr, p_value = stats.pearsonr(merged_data['stringency_index'], merged_data['gdp_change_2020'])
    print(f"Correlation between stringency index and GDP change: {corr:.3f} (p={p_value:.3f})")
    
    # 按大洲分组分析
    continent_analysis = merged_data.groupby('continent').agg({
        'gdp_change_2020': 'mean',
        'gdp_change_2021': 'mean',
        'gdp_change_2022': 'mean',
        'stringency_index': 'mean'
    }).round(2)
    
    print("\nContinent Analysis:")
    print(continent_analysis)
    
    return merged_data

def main():
    # 加载数据
    gdp_data = load_worldbank_data()
    
    # 假设country_impact已经存在
    # 这里需要从之前的分析中加载country_impact数据
    # 或者重新计算country_impact
    
    # 分析GDP影响
    merged_data = analyze_gdp_impact(gdp_data, country_impact)
    
    # 保存处理后的数据
    merged_data.to_csv('processed_data/gdp_impact_analysis.csv', index=False)

if __name__ == "__main__":
    main() 