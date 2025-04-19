import pandas as pd


class CsvMySQL:
    def __init__(self, file):
        self.file = file
        self.df = pd.read_csv(file)

    def getDDL(self):
        pass

    def saveDDL(self):
        pass

    def getTable(self):
        pass

    def createTable(self):
        pass

    def insertData(self):
        pass

def pandas_to_db_type(pd_type):
    """
    将Pandas数据类型映射到数据库字段类型。
    """
    if pd_type == 'int64':
        return 'INT'
    elif pd_type == 'float64':
        return 'FLOAT'
    elif pd_type == 'object':
        return 'VARCHAR(255)'

# 使用示例（请根据实际路径修改）
if __name__ == "__main__":
    filepath = 'data/第一批流水/工商银行/中国工商银行交易明细信息.csv'  # 请替换为实际路径

    # 1. 读取CSV文件
    df = pd.read_csv(filepath, encoding='utf-8')
    columnSeries = df.dtypes
    table_name = 'icbc'
    ddl_columns = []
    for name, dtype in columnSeries.items():
        mysql_type = pandas_to_db_type(dtype)
        ddl_columns.append(f"`{name.strip()}` {mysql_type}")

    ddl = f"CREATE TABLE IF NOT EXISTS {table_name} (\n    " + ",\n    ".join(ddl_columns) + "\n);"
    print("生成的 MySQL DDL 语句如下：")
    print(ddl)



