import os
import csv

# 定义基础目录
base_dir = 'law-data/第一批流水'

# 遍历目录查找工商银行相关的 CSV 文件
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if '工商银行' in file and file.endswith('.csv'):
            file_path = os.path.join(root, file)
            temp_file_path = file_path + '.temp'

            with open(file_path, 'r', encoding='utf-8-sig', newline='') as infile, \
                    open(temp_file_path, 'w', encoding='utf-8', newline='') as outfile:
                reader = csv.reader(infile)
                writer = csv.writer(outfile)

                for row in reader:
                    writer.writerow(row)

            # 替换原文件
            os.replace(temp_file_path, file_path)
            print(f"已处理文件: {file_path}")

