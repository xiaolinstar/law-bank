import os
import csv

# 定义基础目录
base_dir = 'law-data'
# 要排除的文件夹
exclude_folders = ['工会第一批流水拆分', '第六批流水']

# 分别存储不同类型文件的第一行数据和文件路径
file_types = {
    '交易流水.csv': {'first_rows': [], 'file_paths': []},
    '公民身份.csv': {'first_rows': [], 'file_paths': []},
    '银行账户.csv': {'first_rows': [], 'file_paths': []}
}

# 遍历 law-data 目录
for root, dirs, files in os.walk(base_dir):
    # 排除指定文件夹
    dirs[:] = [d for d in dirs if d not in exclude_folders]
    for file in files:
        for file_type in file_types:
            if file.endswith(file_type):
                file_path = os.path.join(root, file)
                file_types[file_type]['file_paths'].append(file_path)
                with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    try:
                        first_row = next(reader)
                        file_types[file_type]['first_rows'].append(first_row)
                        print(f"文件 {file_path} 的第一行数据: {first_row}")
                    except StopIteration:
                        print(f"文件 {file_path} 为空，没有数据。")

# 分别检查不同类型文件第一行数据是否完全一致
for file_type, data in file_types.items():
    first_rows = data['first_rows']
    if first_rows:
        all_same = all(row == first_rows[0] for row in first_rows)
        if all_same:
            print(f"所有 {file_type} 文件的第一行数据完全一致。")
        else:
            print(f"并非所有 {file_type} 文件的第一行数据都一致。")
    else:
        print(f"没有找到符合条件的 {file_type} 文件。")

