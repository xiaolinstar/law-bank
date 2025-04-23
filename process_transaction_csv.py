import os
import csv


def process_csv(file_path):
    # 读取文件
    with open(file_path, 'r', encoding='utf-8', newline='') as infile:
        reader = csv.reader(infile)
        headers = next(reader)  # 读取第一行作为表头
        rows = list(reader)

    # 查找 '查询反馈结果原因' 列的索引
    target_index = None
    for i, header in enumerate(headers):
        if header == '客户名称':
            target_index = i
            break

    if target_index is not None:
        # 删除该列
        new_headers = [header for i, header in enumerate(headers) if i != target_index]
        new_rows = []
        for row in rows:
            new_row = [cell for i, cell in enumerate(row) if i != target_index]
            new_rows.append(new_row)

        # 将处理后的数据写回文件
        with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(new_headers)
            writer.writerows(new_rows)
        print(f"已删除文件 {file_path} 中的 '客户名称' 列")


# 定义基础目录
base_dir = 'law-data'

# 遍历目录查找以 '交易流水.csv' 结尾的文件
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('公民身份.csv'):
            file_path = os.path.join(root, file)
            process_csv(file_path)

