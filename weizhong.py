import csv

# 定义输入文件路径
input_file_path = 'law-data/第三批流水/前海微众银行_交易流水.csv'

# 打开输入文件
with open(input_file_path, 'r', encoding='utf-8', newline='') as infile:
    reader = csv.reader(infile)

    # 读取表头
    headers = next(reader)

    # 查找 '查询反馈结果原因' 列的索引
    target_index = None
    for i, header in enumerate(headers):
        if header == '查询反馈结果原因':
            target_index = i
            break

    if target_index is None:
        print("未找到 '查询反馈结果原因' 列。")
    else:
        # 初始化行号，表头是第 1 行，数据从第 2 行开始
        row_number = 2
        for row in reader:
            if len(row) > target_index and '成功' not in row[target_index]:
                print(f"行号: {row_number}, 行内容: {row}")
            row_number += 1

