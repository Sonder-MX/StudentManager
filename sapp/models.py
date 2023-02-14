from django.db import models

SEX_OPT = (
    (1, '男'),
    (2, '女')
)


# 学生信息
class Student(models.Model):
    Sno = models.CharField(verbose_name="学号", max_length=12, primary_key=True)
    Sname = models.CharField(verbose_name="姓名", max_length=24)
    Ssex = models.SmallIntegerField(verbose_name="性别", choices=SEX_OPT)
    Birthdate = models.DateField(verbose_name="出生日期")
    AdmissionDate = models.DateField(verbose_name="入学时间")
    Sdept = models.CharField(verbose_name="专业名称", max_length=32)
    Sclass = models.CharField(verbose_name="班级", max_length=64)


# 教师信息
class Teacher(models.Model):
    Tno = models.CharField(verbose_name="编号", max_length=12, primary_key=True)
    Tname = models.CharField(verbose_name="姓名", max_length=24)
    Tsex = models.SmallIntegerField(verbose_name="性别", choices=SEX_OPT)
    Birthdate = models.DateField(verbose_name="出生日期")
    EntryDate = models.DateField(verbose_name="入职时间")
    Phone = models.CharField(verbose_name="联系电话", max_length=11)


# 学生账号
class StudAccount(models.Model):
    Saccount = models.OneToOneField(verbose_name="账号", to="Student", to_field="Sno",
                                    on_delete=models.CASCADE, primary_key=True)
    Spwd = models.CharField(verbose_name="密码", max_length=32)


# 教师账号
class TeacAccount(models.Model):
    Taccount = models.OneToOneField(verbose_name="账号", to="Teacher", to_field="Tno",
                                    on_delete=models.CASCADE, primary_key=True)
    Tpwd = models.CharField(verbose_name="密码", max_length=32)


# 课程
class Course(models.Model):
    Cno = models.CharField(verbose_name="课程编号", max_length=12, primary_key=True)
    Cname = models.CharField(verbose_name="课程名称", max_length=24)


# 课表
class Schedulu(models.Model):
    Sid = models.AutoField(primary_key=True)  # 自增id
    Tno = models.ForeignKey(verbose_name="教师编号", to="Teacher", on_delete=models.CASCADE)
    Cno = models.ForeignKey(verbose_name="课程编号", to="Course", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "教师课表"
        verbose_name_plural = verbose_name


# 成绩
class Scores(models.Model):
    SCid = models.AutoField(primary_key=True)
    Sno = models.ForeignKey(verbose_name="学生学号", to="Student", on_delete=models.CASCADE)
    Cno = models.ForeignKey(verbose_name="课程编号", to="Course", on_delete=models.CASCADE)
    Grade = models.IntegerField(verbose_name="成绩")

    class Meta:
        verbose_name = "学生成绩信息"
        verbose_name_plural = verbose_name
