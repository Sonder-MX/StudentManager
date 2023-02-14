import sys
import json
from sqlalchemy import create_engine, MetaData, Table


class DataBasePro:
    def __init__(self, tb_name):
        try:
            self.tb_name = tb_name
            engine = create_engine(f'mysql+pymysql://{user_name}:{user_pwd}@localhost:3306/{db_name}?charset=utf8')
            metadata = MetaData(engine)  # 绑定引擎
            self.__table = Table(tb_name, metadata, autoload=True)  # 连接数据表
            self.__conn = engine.connect()  # 连接引擎
        except RuntimeError:
            print('数据库连接错误！！！')

    def commit_data(self, data: list[dict]):
        try:
            self.__conn.execute(self.__table.insert(), data)
            print(f'表 {self.tb_name} 数据存储成功')
        except Exception as e:
            print(f'表 {self.tb_name} 数据存储失败！！！')
            print(e)
        finally:
            self.__conn.close()


def insert_data(data: dict):
    for table in data:
        table_name = f"sapp_{table}"
        fields = data[table]["fields"]
        table_data = data[table]['data']
        data_list = [dict(zip(fields, line)) for line in table_data]
        # print(data_list)
        DataBasePro(table_name).commit_data(data_list)


def test_data() -> dict:
    with open('SqlScript/data.json', 'r', encoding='utf-8') as rf:
        json_data = json.load(rf)
        return json_data


if __name__ == '__main__':
    db_name = 'StudentManager'
    params = sys.argv[1:]
    if len(params) > 3 or len(params) < 2:
        print("Error:")
        print("  使用默认数据库(StudentManager) >: 'python insert_test_data.py 数据库用户名 数据库密码'")
        print("  使用自定义数据库 >: 'python insert_test_data.py 数据库用户名 数据库密码 数据库名称'")
        exit(1)
    user_name = params[0]
    user_pwd = params[1]
    if len(params) == 3:
        db_name = params[2]
    insert_data(test_data())
