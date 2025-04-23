import os
import pandas as pd
from pathlib import Path


def xlsx_to_csv_converter(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.xlsx'):
                file_path = Path(root) / file
                output_dir = Path(root) / "csv_output"
                output_dir.mkdir(exist_ok=True)

                try:
                    # 读取Excel文件（自动处理中文路径）
                    xls = pd.ExcelFile(file_path, engine='openpyxl')

                    # 转换每个工作表
                    for sheet_name in xls.sheet_names:
                        # 读取工作表数据
                        df = pd.read_excel(xls, sheet_name=sheet_name)

                        # 生成CSV文件名
                        csv_filename = f"{file_path.stem}_{sheet_name}.csv"
                        csv_path = output_dir / csv_filename

                        # 写入CSV（使用UTF-8-SIG编码防止中文乱码）
                        df.to_csv(
                            csv_path,
                            index=False,
                            encoding='utf-8',
                            errors='strict'
                        )
                        print(f"转换成功：{file_path} -> {csv_path}")

                except Exception as e:
                    print(f"转换失败 {file_path}: {str(e)}")


if __name__ == "__main__":
    target_dir = 'data'
    if Path(target_dir).is_dir():
        xlsx_to_csv_converter(target_dir)
        print("全部转换完成！CSV文件保存在各子目录的csv_output文件夹中")
    else:
        print("错误：输入的路径不是有效目录")
