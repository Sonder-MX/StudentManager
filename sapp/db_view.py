"""
使用 MySQL 视图
"""
from sapp.models import *


# 学生成绩表
class StudentGradeTable(models.Model):
    Sno = models.CharField(verbose_name="学号", max_length=12, primary_key=True)
    Sname = models.CharField(verbose_name="姓名", max_length=24)
    Sdept = models.CharField(verbose_name="专业名称", max_length=32)
    Sclass = models.CharField(verbose_name="班级", max_length=64)
    Cname = models.CharField(verbose_name="课程名称", max_length=24)
    Grade = models.IntegerField(verbose_name="成绩")
    Tname = models.CharField(verbose_name="姓名", max_length=24)
    Phone = models.CharField(verbose_name="联系电话", max_length=11)

    class Meta:
        db_table = "grade_table"


# 教师-学生成绩
class TeacherGrade(models.Model):
    Tno = models.CharField(verbose_name="教师编号", max_length=12, primary_key=True)
    Tname = models.CharField(verbose_name="教师姓名", max_length=24)
    Cno_id = models.CharField(verbose_name="课程编号", max_length=12)
    Cname = models.CharField(verbose_name="课程名称", max_length=24)
    Sno = models.CharField(verbose_name="学生学号", max_length=12)
    Sname = models.CharField(verbose_name="学生姓名", max_length=24)
    Sdept = models.CharField(verbose_name="专业", max_length=32)
    Sclass = models.CharField(verbose_name="班级", max_length=64)
    Grade = models.IntegerField(verbose_name="成绩")

    class Meta:
        db_table = "teacher_grade"
