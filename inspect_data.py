import pandas as pd

# 读取数据
df = pd.read_csv('owid-covid-data.csv')

# 显示数据基本信息
print("数据形状:", df.shape)
print("\n列名:", df.columns.tolist())
print("\n数据预览:")
print(df.head())
print("\n数据类型和非空值统计:")
print(df.info()) 