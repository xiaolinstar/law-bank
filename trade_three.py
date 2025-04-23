import os

# 定义第七批流水文件夹路径
base_dir = 'law-data/第七批流水'

# 检查目录是否存在
if os.path.isdir(base_dir):
    # 遍历目录下的所有文件
    for file_name in os.listdir(base_dir):
        file_path = os.path.join(base_dir, file_name)
        # 检查文件名是否以 第七批流水_ 开头且以 .csv 结尾
        if file_name.startswith('第七批流水_') and file_name.endswith('.csv'):
            # 提取银行名称
            bank_name = file_name.replace('第七批流水_', '').replace('.csv', '')
            # 生成新的文件名
            new_file_name = f"{bank_name}_交易流水.csv"
            new_file_path = os.path.join(base_dir, new_file_name)
            # 重命名文件
            os.rename(file_path, new_file_path)
else:
    print(f"目录 {base_dir} 不存在。")