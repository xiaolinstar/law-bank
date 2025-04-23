import os
import csv

# 定义基础目录
base_dir = 'law-data'

# 遍历目录查找以 '交易流水.csv' 结尾的文件
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('交易流水.csv'):
            file_path = os.path.join(root, file)
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                    reader = csv.DictReader(csvfile)
                    fieldnames = reader.fieldnames
                    rows = []
                    for row in reader:
                        if row.get('对手交易余额') == '':
                            row['对手交易余额'] = '0.00'
                        rows.append(row)

                # 将修改后的数据写回文件
                with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(rows)

                print(f"文件 {file_path} 处理完成")
            except FileNotFoundError:
                print(f"未找到文件: {file_path}")
            except Exception as e:
                print(f"处理文件 {file_path} 时发生错误: {e}")
