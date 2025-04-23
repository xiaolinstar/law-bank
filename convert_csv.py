import os
import chardet
from pathlib import Path


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)  # 读取前 10000 字节用于检测编码
        result = chardet.detect(raw_data)
        return result['encoding']


def convert_to_utf8(file_path, original_encoding):
    try:
        # 读取文件内容（使用更兼容的GB18030编码）
        with open(file_path, 'r', encoding=original_encoding, errors='strict') as f:
            content = f.read()

        # 写回UTF-8编码（不带BOM）
        with open(file_path, 'w', encoding='utf-8', errors='strict', newline='') as f:
            f.write(content)

        print(f"成功转换：{file_path}")
        return True
    except Exception as e:
        print(f"转换失败 {file_path}: {str(e)}")
        return False


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = Path(root) / file
                print(f"正在处理：{file_path}")

                # 检测原始编码
                encoding = detect_encoding(file_path)
                print(f"检测到编码：{encoding}")

                # 如果已经是UTF编码则跳过
                if encoding and encoding.lower().startswith('utf'):
                    print(f"已跳过（已经是UTF编码）：{file_path}")
                    continue

                # 处理常见中文编码兼容性
                if encoding in ['GB2312', 'GBK']:
                    encoding = 'GB18030'  # 使用更兼容的编码

                # 尝试转换
                if not convert_to_utf8(file_path, encoding):
                    # 如果转换失败，尝试用GB18030再次转换
                    print("尝试使用GB18030重新转换...")
                    convert_to_utf8(file_path, 'GB18030')


if __name__ == "__main__":
    target_dir = 'data'
    if Path(target_dir).is_dir():
        process_directory(target_dir)
        print("转换完成！")
    else:
        print("错误：输入的路径不是有效目录")
