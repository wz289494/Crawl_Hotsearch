import pandas as pd
import pymysql

class Store(object):
    """
    Store is a class designed to store extracted data into MySQL and Excel.

    Methods:
        mode_mysql(db_name, tb_name): Stores data into a MySQL database.
        mode_excel(excel_name): Stores data into an Excel file.
    """

    def __init__(self, data_list):
        """
        Initializes the Store class with a list of data.

        Args:
            data_list (list): The list of data to store.
        """
        self.data_list = data_list

    def mode_mysql(self, db_name, tb_name):
        """
        Stores data into a MySQL database.

        Args:
            db_name (str): The name of the database.
            tb_name (str): The name of the table.
        """
        try:
            # 连接数据库
            self.db = pymysql.connect(host='localhost', user='root', passwd='wz131', port=3306)
            self.cursor = self.db.cursor()
            print('-连接成功-')

            # 检查并创建数据库（如果不存在）
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            print('-数据库已检查-')

            # 选择数据库
            self.cursor.execute(f"USE {db_name}")

            # 创建数据表
            self.__create_table(tb_name)

            # 插入数据
            self.__insert(tb_name)
            # print('-正在插入数据-')

            # 关闭mysql
            self.db.close()
            print('-连接关闭-')

        except pymysql.MySQLError as e:
            print(f"连接数据库时出现错误：{e}")

    def __create_table(self, tb_name):
        """
        Creates a table in the MySQL database if it doesn't exist.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {tb_name} (
                ID INT AUTO_INCREMENT PRIMARY KEY,
                title Text,
                hotcount Text,
                link Text,
                platform VARCHAR(50),
                slist VARCHAR(50),
                rectime DATETIME
            );
            """
            self.cursor.execute(create_table_query)
            print('-表已检查-')

        except pymysql.MySQLError as e:
            print(f"创建数据表时出现错误：{e}")

    def __insert(self, tb_name):
        """
        Inserts data into the MySQL table.

        Args:
            tb_name (str): The name of the table.
        """
        try:
            insert_query = f"""
            INSERT INTO {tb_name} (title, hotcount, link, platform, slist, rectime)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            # 执行多条插入，每个元素是一个字典
            for post in self.data_list:
                self.cursor.execute(insert_query, (
                    post['title'], post['hotcount'], post['link'],
                    post['platform'], post['slist'], post['rectime']
                ))

            self.db.commit()
            print('-数据插入成功-')

        except pymysql.MySQLError as e:
            print(f"执行插入操作时出现错误：{e}")
            self.db.rollback()

    def mode_excel(self, excel_name):
        """
        Stores data into an Excel file.

        Args:
            excel_name (str): The name of the Excel file.
        """
        try:
            df = pd.DataFrame(self.data_list)
            df.to_excel(excel_name, index=False)
            print('数据已保存到Excel文件！')

        except Exception as e:
            print(f"保存到Excel文件时出现错误：{e}")
