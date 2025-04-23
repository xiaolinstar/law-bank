import os

law_data_path = 'law-data'
result = []
if os.path.isdir(law_data_path):
    for root, dirs, files in os.walk(law_data_path):
        for file in files:
            if file.endswith('交易流水.csv'):
                f = os.path.join(root, file)
                [a, b] = root.split('\\')
                fstr = f"""
LOAD DATA INFILE '/var/lib/mysql-files/{b}/{file}'
INTO TABLE slip
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES;
"""
                print(fstr)

                result.append(os.path.join(root, file))

# for line in result:
#     print(line)

# print(result)

