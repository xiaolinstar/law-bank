import os
import re

# 定义第二批流水文件夹路径
base_dir = 'law-data/第二批流水'

# 检查目录是否存在
if os.path.isdir(base_dir):
    # 遍历目录下的所有文件
    for file_name in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file_name)
        # 使用正则表达式匹配以 _银行名.csv 结尾的文件
        match = re.search(r'_([^_]+)\.csv$', file_name)
        if match:
            bank_name = match.group(1)
            # 生成新的文件名
            new_file_name = f"{bank_name}_交易流水.csv"
            new_file_path = os.path.join(base_dir, new_file_name)
            # 重命名文件
            os.rename(file_path, new_file_path)
else:
    print(f"目录 {base_dir} 不存在。")
