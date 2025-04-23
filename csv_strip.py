import os
import csv

def process_csv_files(folder_path):
    """
    递归遍历指定文件夹下的所有CSV文件，读取文件内容，
    去掉双引号以及前后多余的空白符，并保存处理后的数据。
    :param folder_path: 要遍历的文件夹路径
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('公民身份.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                # 读取CSV文件内容
                with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    rows = [row for row in reader]

                # 处理每一行数据
                processed_rows = []
                for row in rows:
                    processed_row = [cell.strip().replace('"', '') for cell in row]
                    processed_rows.append(processed_row)

                # 将处理后的数据写回文件
                with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(processed_rows)

                print(f"Processed and saved: {file_path}")

def process_csv_files(folder_path):
    """
    递归遍历指定文件夹下的所有CSV文件，读取文件内容，
    去掉双引号以及前后多余的空白符，将每一行数据与表头一一对应，多余数据删除，
    并保存处理后的数据。
    :param folder_path: 要遍历的文件夹路径
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('公民身份.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                # 读取CSV文件内容
                with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    rows = [row for row in reader]

                if not rows:
                    continue

                # 获取表头
                header = rows[0]
                header_length = len(header)

                # 处理每一行数据
                processed_rows = [header]  # 先添加表头
                for row in rows[1:]:
                    processed_row = [cell.strip().replace('"', '') for cell in row]
                    # 截取与表头长度一致的数据
                    processed_row = processed_row[:header_length]
                    processed_rows.append(processed_row)

                # 将处理后的数据写回文件
                with open(file_path, 'w', newline='', encoding='utf-8') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerows(processed_rows)

                print(f"Processed and saved: {file_path}")


def csv_walk(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('公民身份.csv'):
                file_path = os.path.join(root, file)
                print(f"Processing file: {file_path}")

                # 读取CSV文件内容
                with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                    reader = csv.reader(infile)
                    rows = [row for row in reader]
                    for line in rows:
                        print(len(line), line)



# 示例用法
if __name__ == "__main__":
    folder = 'law-data/第二批流水'
    csv_walk(folder)
