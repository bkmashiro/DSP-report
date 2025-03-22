import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager
import statsmodels.api as sm
from statsmodels.graphics.gofplots import qqplot
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体支持


def setup_chinese_fonts():
    """设置支持中文显示的字体"""
    font_dirs = ["./fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    # 设置默认字体
    plt.rcParams['font.family'] = ['Noto Sans SC', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据加载和预处理


def load_and_preprocess_data(file_path='owid-covid-data.csv'):
    """加载并预处理COVID-19数据集"""
    # 读取数据
    df = pd.read_csv(file_path)

    # 转换日期列
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter

    return df

# 数据清洗函数


def clean_data(df):
    """基本数据清洗"""
    # 复制数据框以避免修改原始数据
    df_clean = df.copy()

    # 检查并处理缺失值
    print("原始数据形状:", df.shape)
    print("缺失值比例:")
    missing_percentage = df.isnull().mean() * 100
    print(missing_percentage[missing_percentage >
          0].sort_values(ascending=False))

    # 删除所有记录为空的列（如果有的话）
    df_clean = df_clean.dropna(axis=1, how='all')

    # 删除关键列(location, date, total_cases, total_deaths)中有缺失值的行
    key_columns = ['location', 'date']
    df_clean = df_clean.dropna(subset=key_columns)

    print("\n清洗后数据形状:", df_clean.shape)

    return df_clean

# 创建国家/地区数据子集


def get_country_data(df, country):
    """获取指定国家/地区的数据子集"""
    return df[df['location'] == country].copy()

# 创建多国家/地区数据子集


def get_countries_data(df, countries):
    """获取多个国家/地区的数据子集"""
    return df[df['location'].isin(countries)].copy()

# 创建大洲数据子集


def get_continent_data(df, continent):
    """获取指定大洲的数据子集"""
    return df[df['continent'] == continent].copy()

# 数据汇总函数


def summarize_by_date(df, date_col='date', freq='M', agg_dict=None):
    """
    按指定日期频率汇总数据

    参数:
    df : DataFrame - 输入的数据框
    date_col : str - 日期列名，默认为 'date'
    freq : str - 重采样频率 ('D'日, 'W'周, 'M'月, 'Q'季, 'Y'年)
    agg_dict : dict - 自定义聚合方法字典

    返回:
    DataFrame - 按指定频率汇总后的数据
    """
    # 确保日期列为datetime类型
    df[date_col] = pd.to_datetime(df[date_col])

    # 设置日期为索引
    df_temp = df.set_index(date_col)

    # 如果没有提供聚合方法字典，自动生成
    if agg_dict is None:
        agg_dict = {}
        for column in df_temp.columns:
            # 获取列的数据类型
            dtype = df_temp[column].dtype
            dtype_str = str(dtype)  # 转换为字符串进行判断

            # 根据数据类型选择合适的聚合方法
            if ('int' in dtype_str.lower() or
                'float' in dtype_str.lower() or
                    'number' in dtype_str.lower()):  # 数值型数据
                agg_dict[column] = 'mean'  # 数值取平均
            elif dtype_str == 'object' or 'string' in dtype_str.lower():  # 文本数据
                agg_dict[column] = 'first'  # 文本取第一个值
            elif 'datetime' in dtype_str.lower():  # 日期类型
                agg_dict[column] = 'first'  # 日期取第一个值
            else:
                agg_dict[column] = 'first'  # 其他类型默认取第一个值

    # 按日期频率重采样并使用指定的聚合方法
    df_resampled = df_temp.resample(freq).agg(agg_dict)

    return df_resampled.reset_index()

# 绘图辅助函数


def plot_time_series(df, x_col, y_col, title, xlabel, ylabel, figsize=(12, 6), color='blue', alpha=0.7):
    """绘制时间序列图"""
    plt.figure(figsize=figsize)
    plt.plot(df[x_col], df[y_col], color=color, alpha=alpha)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


def plot_multi_time_series(df, x_col, y_col, group_col, title, xlabel, ylabel, figsize=(14, 7)):
    """绘制多条时间序列图（按分组）"""
    plt.figure(figsize=figsize)

    for name, group in df.groupby(group_col):
        plt.plot(group[x_col], group[y_col],
                 label=name, linewidth=2, alpha=0.7)

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


def plot_correlation_heatmap(df, columns, title, figsize=(12, 10)):
    """绘制相关性热力图"""
    # 计算相关系数矩阵
    corr_matrix = df[columns].corr()

    # 创建掩码，只显示下三角矩阵
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # 绘制热力图
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, cbar_kws={"shrink": .8})
    plt.title(title, fontsize=14)
    plt.tight_layout()


def plot_regression(x, y, title, xlabel, ylabel, figsize=(10, 6)):
    """绘制回归分析图"""
    # 添加常数项
    X = sm.add_constant(x)

    # 拟合回归模型
    model = sm.OLS(y, X).fit()

    # 获取摘要
    print(model.summary())

    # 预测值
    predictions = model.predict(X)

    # 绘图
    plt.figure(figsize=figsize)
    plt.scatter(x, y, alpha=0.7)
    plt.plot(x, predictions, 'r', alpha=0.7)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return model

# 时间序列预测模型


def fit_arima_model(series, order=(1, 1, 1)):
    """拟合ARIMA模型"""
    model = ARIMA(series, order=order)
    result = model.fit()
    return result


def forecast_future(model, steps=30):
    """使用拟合好的模型进行预测"""
    forecast = model.forecast(steps=steps)
    return forecast


def plot_frequency_distribution(df, variables, subplots_cols=2, subplots_rows=2):
    """绘制频率分布图"""
    # 创建子图
    fig, axes = plt.subplots(subplots_rows, subplots_cols, figsize=(15, 12))
    axes = axes.ravel()


    for idx, var in enumerate(variables):
        data = df[var].dropna()
        q95 = np.percentile(data, 95)
        data = data[data <= q95]
        
        # 使用更高效的绘图方法
        axes[idx].hist(data, bins=50, density=True, alpha=0.6)
        
        # 添加基本统计信息
        stats_text = f'data statistics (95% quantile):\n'
        stats_text += f'mean: {data.mean():.2f}\n'
        stats_text += f'median: {data.median():.2f}\n'
        stats_text += f'sample size: {len(data):,}'
        
        axes[idx].text(0.95, 0.95, stats_text,
                    transform=axes[idx].transAxes,
                    verticalalignment='top',
                    horizontalalignment='right',
                    bbox=dict(facecolor='white', alpha=0.8))
        
        axes[idx].set_title(f'{var} freq diagram (95% quantile)')
        axes[idx].set_xlabel(var)
        axes[idx].set_ylabel('density')

    plt.tight_layout()
    plt.show()
