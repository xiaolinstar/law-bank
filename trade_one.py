import os
import shutil

# 定义 law-data 文件夹路径
base_dir = 'law-data/第一批流水'

# 遍历 law-data 下的所有文件夹
for root, dirs, files in os.walk(base_dir):
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        # 遍历文件夹内的所有文件
        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)
            # 生成新的文件名
            new_file_name = f"{dir_name}_{file_name}"
            new_file_path = os.path.join(base_dir, new_file_name)
            # 移动文件
            shutil.move(file_path, new_file_path)
    
    # 删除空文件夹
    for dir_name in dirs:
        dir_path = os.path.join(root, dir_name)
        if not os.listdir(dir_path):
            os.rmdir(dir_path)
