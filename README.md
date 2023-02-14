# 学生管理成绩系统

## 1.环境准备

### （1）配置环境

|  应用  |  版本  |
| :----: | :----: |
| Python | 3.11.0 |
| MySQL  | 8.0.28 |



### （2）Requirement

- `pip install django==4.1.4`
- `pip install sqlalchemy==1.4.44`



### （3）Plugins

- jquery==3.6.1
- bootstarp==5



## 2.快速开始

1. 创建数据库 `StudentManager`

   进入终端，执行以下命令：

   `mysql -uroot -p密码`

   进入MySQL终端后，执行以下命令：

   `CREATE DATABASE IF NOT EXISTS StudentManager DEFAULT CHARSET utf8 COLLATE utf8_general_ci;`

   用命令 `SHOW DATABASES;` 查看数据库StudentManager是否创建成功。

   

2. 修改数据库配置

   cd到当前文件夹，进入 StudentManager 文件夹，修改 `settings.py` 配置文件中的 `DATABASES`

   数据库名称为第1步创建成功的数据库名称，密码修改为你设置的数据库密码。

   ```python
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'StudentManager',
            'HOST': '127.0.0.1',
            'PORT': 3306,
            'USER': 'root',
            'PASSWORD': '数据库密码',
        }
    }
   ```

   

3. 创建数据表(一)

   进入 sapp 文件夹，修改 `models.py` 文件，增加以下内容：

   ```python
   ```

   

4. 创建数据表(二)

   cd到存在 `manager.py` 的文件下，依次执行以下命令：

   - 生成迁移文件 `python manage.py makemigrations`

   - 同步到数据库 `python manage.py migrate`

   

5. 增加测试数据

   进入 `SqlScript` 文件夹下

   

6. 启动 Django

   cd到存在 `manager.py` 的文件下，执行命令

   `python manager.py runserver`

   在浏览器中输入 http://127.0.0.1:8000/login/ 

   Enjoy！

