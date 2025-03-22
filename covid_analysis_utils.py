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

# Set up Chinese font support


def setup_chinese_fonts():
    """Set up fonts that support Chinese display"""
    font_dirs = ["./fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    # Set default font
    plt.rcParams['font.family'] = ['Noto Sans SC', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display issue

# Data loading and preprocessing


def load_and_preprocess_data(file_path='owid-covid-data.csv'):
    """Load and preprocess COVID-19 dataset"""
    # Read data
    df = pd.read_csv(file_path)

    # Convert date column
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['week'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter

    return df

# Data cleaning functions


def clean_data(df):
    """Basic data cleaning"""
    # Copy dataframe to avoid modifying original data
    df_clean = df.copy()

    # Check and handle missing values
    print("Original data shape:", df.shape)
    print("Missing value percentage:")
    missing_percentage = df.isnull().mean() * 100
    print(missing_percentage[missing_percentage >
          0].sort_values(ascending=False))

    # Remove columns that are entirely empty (if any)
    df_clean = df_clean.dropna(axis=1, how='all')

    # Remove rows with missing values in key columns (location, date)
    key_columns = ['location', 'date']
    df_clean = df_clean.dropna(subset=key_columns)

    print("\nCleaned data shape:", df_clean.shape)

    return df_clean

# Create country/region data subsets


def get_country_data(df, country):
    """Get data subset for specified country/region"""
    return df[df['location'] == country].copy()

# Create multi-country/region data subsets


def get_countries_data(df, countries):
    """Get data subset for multiple countries/regions"""
    return df[df['location'].isin(countries)].copy()

# Create continent data subsets


def get_continent_data(df, continent):
    """Get data subset for specified continent"""
    return df[df['continent'] == continent].copy()

# Data summary functions


def summarize_by_date(df, date_col='date', freq='M', agg_dict=None):
    """
    Summarize data by specified date frequency

    Parameters:
    df : DataFrame - Input dataframe
    date_col : str - Date column name, default is 'date'
    freq : str - Resampling frequency ('D' daily, 'W' weekly, 'M' monthly, 'Q' quarterly, 'Y' yearly)
    agg_dict : dict - Custom aggregation method dictionary

    Returns:
    DataFrame - Data summarized by specified frequency
    """
    # Ensure date column is datetime type
    df[date_col] = pd.to_datetime(df[date_col])

    # Set date as index
    df_temp = df.set_index(date_col)

    # If no aggregation dictionary provided, auto-generate one
    if agg_dict is None:
        agg_dict = {}
        for column in df_temp.columns:
            # Get column data type
            dtype = df_temp[column].dtype
            dtype_str = str(dtype)  # Convert to string for comparison

            # Choose appropriate aggregation method based on data type
            if ('int' in dtype_str.lower() or
                'float' in dtype_str.lower() or
                    'number' in dtype_str.lower()):  # Numeric data
                agg_dict[column] = 'mean'  # Take mean for numbers
            elif dtype_str == 'object' or 'string' in dtype_str.lower():  # Text data
                agg_dict[column] = 'first'  # Take first value for text
            elif 'datetime' in dtype_str.lower():  # Date type
                agg_dict[column] = 'first'  # Take first value for dates
            else:
                agg_dict[column] = 'first'  # Default to first value for other types

    # Resample by date frequency and apply specified aggregation methods
    df_resampled = df_temp.resample(freq).agg(agg_dict)

    return df_resampled.reset_index()

# Plotting helper functions


def plot_time_series(df, x_col, y_col, title, xlabel, ylabel, figsize=(12, 6), color='blue', alpha=0.7):
    """Plot time series graph"""
    plt.figure(figsize=figsize)
    plt.plot(df[x_col], df[y_col], color=color, alpha=alpha)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()


def plot_multi_time_series(df, x_col, y_col, group_col, title, xlabel, ylabel, figsize=(14, 7)):
    """Plot multiple time series graphs (by group)"""
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
    """Plot correlation heatmap"""
    # Calculate correlation coefficient matrix
    corr_matrix = df[columns].corr()

    # Create mask to only show lower triangle matrix
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # Plot heatmap
    plt.figure(figsize=figsize)
    sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                linewidths=0.5, cbar_kws={"shrink": .8})
    plt.title(title, fontsize=14)
    plt.tight_layout()


def plot_regression(x, y, title, xlabel, ylabel, figsize=(10, 6)):
    """Plot regression analysis graph"""
    # Add constant term
    X = sm.add_constant(x)

    # Fit regression model
    model = sm.OLS(y, X).fit()

    # Get summary
    print(model.summary())

    # Predicted values
    predictions = model.predict(X)

    # Plot
    plt.figure(figsize=figsize)
    plt.scatter(x, y, alpha=0.7)
    plt.plot(x, predictions, 'r', alpha=0.7)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    return model

# Time series prediction models


def fit_arima_model(series, order=(1, 1, 1)):
    """Fit ARIMA model"""
    model = ARIMA(series, order=order)
    result = model.fit()
    return result


def forecast_future(model, steps=30):
    """Make predictions using fitted model"""
    forecast = model.forecast(steps=steps)
    return forecast


def plot_frequency_distribution(df, variables, subplots_cols=2, subplots_rows=2):
    """Plot frequency distribution"""
    # Create subplots
    fig, axes = plt.subplots(subplots_rows, subplots_cols, figsize=(15, 12))
    axes = axes.ravel()

    for idx, var in enumerate(variables):
        data = df[var].dropna()
        q95 = np.percentile(data, 95)
        data = data[data <= q95]
        
        # Use more efficient plotting method
        axes[idx].hist(data, bins=50, density=True, alpha=0.6)
        
        # Add basic statistical information
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
