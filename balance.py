import os
import pandas as pd

# 定义 law-data 文件夹路径
law_data_path = 'law-data'

# 遍历 law-data 文件夹及其子文件夹
for root, dirs, files in os.walk(law_data_path):
    for file in files:
        if file.endswith('交易流水.csv'):
            file_path = os.path.join(root, file)
            try:
                # 读取 CSV 文件
                df = pd.read_csv(file_path)


                # 检查是否存在 可用余额 和 账户余额 列
                if '交易金额' in df.columns or '交易余额' in df.columns:
                    # 将 可用余额 和 账户余额 为空的单元格设置为 0.00
                    df['交易金额'] = df['交易金额'].fillna('NULL')
                    df['交易余额'] = df['交易余额'].fillna('NULL')
                    # 将修改后的数据保存回原文件
                    df.to_csv(file_path, index=False)
                    print(f'已处理文件: {file_path}')

            except Exception as e:
                print(f'处理文件 {file_path} 时出错: {e}')

