import pandas as pd
from typing import Generator, List, Any
from datetime import datetime


class CsvToSQLConverter:
    def __init__(self, csv_path: str, table_name: str, db_dialect: str = "mysql",
                 delimiter: str = ",", encoding: str = "utf-8",
                 date_formats: list = None):
        """
        构造方法
        :param csv_path: CSV文件路径
        :param table_name: 目标表名
        :param db_dialect: 数据库类型（mysql/postgresql/sqlite）
        :param delimiter: CSV分隔符
        :param encoding: 文件编码
        :param date_formats: 可选日期格式列表
        """
        self.csv_path = csv_path
        self.table_name = table_name
        self.db_dialect = db_dialect
        self.delimiter = delimiter
        self.encoding = encoding
        self.date_formats = date_formats if date_formats else []
        self.df = self._read_csv()

    def set_column_types(self, type_overrides: dict):
        """
        设置自定义列类型（覆盖自动推断）
        :param type_overrides: {列名: 数据类型}
        """
        self.type_overrides = type_overrides

    def generate_ddl(self, drop_if_exists: bool = True,
                    engine: str = 'InnoDB', charset: str = 'utf8mb4', comment: str = None) -> str:
        """
        生成 CREATE TABLE语句
        :param drop_if_exists: 是否添加DROP TABLE语句
        :param engine: 存储引擎（MySQL专用）
        :param charset: 字符集设置
        :param comment: 表注释
        :return: SQL字符串
        """
        ddl = ""
        if drop_if_exists:
            ddl += f"DROP TABLE IF EXISTS {self.table_name};\n"

        column_types = self._infer_column_types()
        if hasattr(self, 'type_overrides'):
            column_types.update(self.type_overrides)

        columns = []
        for col_name, col_type in column_types.items():
            # 删除数据前后的空字符，包括空格、制表符等
            columns.append(f"`{col_name}` {col_type}")

        # 生成CREATE TABLE语句
        create_table = f"CREATE TABLE {self.table_name} (\n"
        create_table += ",\n".join(columns)
        create_table += "\n)"

        if self.db_dialect == "mysql" and engine:
            create_table += f" ENGINE={engine}"
        if self.db_dialect == "mysql" and charset:
            create_table += f" DEFAULT CHARSET={charset}"
        if self.db_dialect == 'mysql' and comment:
            create_table += f" COMMENT={comment}"

        create_table += ";"
        ddl += create_table
        return ddl

    def generate_inserts(self, batch_size: int = 100,
                        on_duplicate: str = None) -> Generator[str, None, None]:
        """
        生成INSERT语句生成器
        :param batch_size: 批量插入记录数
        :param on_duplicate: 重复处理策略（如MySQL的ON DUPLICATE KEY UPDATE）
        :return: 生成器产出SQL语句
        """
        columns = ', '.join([f'`{col}`' for col in self.columns])
        for i in range(0, len(self.df), batch_size):
            batch = self.df.iloc[i:i + batch_size]
            values_list = []
            for _, row in batch.iterrows():
                sanitized_values = []
                for col in self.columns:
                    column_type_dict = self._infer_column_types()
                    col_type = column_type_dict.get(col)
                    value = self._sanitize_value(str(row[col]), col_type)
                    sanitized_values.append(value)
                values_str = "(" + ", ".join(sanitized_values) + ")"
                values_list.append(values_str)

            insert_stmt = f"INSERT INTO {self.table_name} ({columns}) VALUES "
            insert_stmt += ",\n".join(values_list)
            if on_duplicate:
                insert_stmt += f" {on_duplicate}"
            insert_stmt += ";"
            yield insert_stmt

    def export_sql_file(self, output_path: str,
                       include_ddl: bool = True,
                       batch_size: int = 500) -> None:
        """
        导出完整SQL文件
        :param output_path: 输出文件路径
        :param include_ddl: 是否包含DDL语句
        :param batch_size: 批量插入大小
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            if include_ddl:
                ddl = self.generate_ddl()
                f.write(ddl + '\n')
            load_sql = f"""
LOAD DATA INFILE 'example.csv'
INTO TABLE example_table
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\\r\\n'
IGNORE 1 LINES;
"""
            f.write(load_sql + '\n')
            # for insert in self.generate_inserts(batch_size=batch_size):
            #     f.write(insert + '\n')

    def _read_csv(self) -> pd.DataFrame:
        """内部方法：读取并解析CSV文件"""
        res = pd.read_csv(self.csv_path, delimiter=self.delimiter, encoding=self.encoding)
        res.columns = res.columns.str.strip()
        for col in res.columns:
            if res[col].dtype == 'object':
                res[col] = res[col].str.strip()
        return res

    def _infer_column_types(self, sample_size: int = 1000) -> dict:
        """
        推断列数据类型
        :param sample_size: 用于推断的采样行数
        :return: 类型字典 {列名: 类型}
        """
        sample = self.df.head(sample_size)

        column_types = {}
        for col in sample.columns:
            col_type = sample[col].dtype
            if pd.api.types.is_integer_dtype(col_type):
                column_types[col] = "BIGINT"
            elif pd.api.types.is_float_dtype(col_type):
                column_types[col] = "DECIMAL(10,2)"
            elif pd.api.types.is_datetime64_dtype(col_type):
                column_types[col] = "DATETIME"
            else:
                max_length = sample[col].astype(str).str.len().max()
                if max_length is None:
                    max_length = 255
                column_types[col] = f"VARCHAR({max(max_length, 255)})"
        return column_types

    def _sanitize_value(self, value: str, col_type: str) -> str:
        """
        数据值清洗和转义
        :param value: 原始值
        :param col_type: 目标列类型
        :return: 转义后的安全值
        """
        if value.lower() == 'nan' or value.lower() == 'none':
            return "NULL"
        if 'INT' in col_type or 'FLOAT' in col_type:
            return value
        if 'DATETIME' in col_type:
            for fmt in self.date_formats:
                try:
                    datetime.strptime(value, fmt)
                    return "'{}'".format(value)
                except ValueError:
                    continue
            return "NULL"
        sanitized = value.replace("'", "''")
        return "'{}'".format(sanitized)

    @staticmethod
    def _detect_date_format(value: str, formats: list) -> Any | None:
        """
        检测日期格式
        :param value: 日期字符串
        :param formats: 候选格式列表
        :return: 匹配的格式或None
        """
        for fmt in formats:
            try:
                datetime.strptime(value, fmt)
                return fmt
            except ValueError:
                continue
        return None

    @property
    def columns(self) -> List[str]:
        """获取列名列表"""
        res = []
        if self.df is not None:
            for col in self.df.columns:
                res.append(col.strip())
        return res

    @property
    def row_count(self) -> int:
        """获取总行数统计"""
        if self.df is not None:
            return len(self.df)
        return 0




if __name__ == '__main__':

    files = ['data/第一批流水/工商银行/公民身份.csv', 'data/第一批流水/工商银行/交易流水.csv', 'data/第一批流水/工商银行/银行账号.csv']
    tables = ['icbc_person', 'icbc_trade', 'icbc_account']

    for idx, file in enumerate(files):
        # 假设 CSV 文件路径，你需要根据实际情况修改
        csv_file_path = file
        table_name = tables[idx]

        # 创建 CsvToSQLConverter 实例
        converter = CsvToSQLConverter(csv_path=csv_file_path, table_name=table_name)

        # 生成并输出 DDL 语句
        example_ddl = converter.generate_ddl()
        converter.export_sql_file('{}.sql'.format(table_name))
