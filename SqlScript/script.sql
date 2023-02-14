/* 创建 StudentManger 数据库 */
DROP DATABASE IF EXISTS StudentManager;
CREATE DATABASE StudentManager;


/* 添加测试数据 */
-- python SqlScript/insert_test_data.py 数据库账号 数据库密码


/* 创建视图 */
USE StudentManager;

DROP VIEW IF EXISTS grade_table;
CREATE VIEW grade_table
AS
SELECT sapp_student.Sno,Sname,Sdept,Sclass,Cname,Grade,Tname,Phone
FROM sapp_student,sapp_scores,sapp_course,sapp_schedulu,sapp_Teacher
WHERE sapp_student.Sno=sapp_scores.Sno_id
AND sapp_scores.Cno_id=sapp_course.Cno
AND sapp_scores.Cno_id=sapp_schedulu.Cno_id
AND sapp_schedulu.Tno_id=sapp_Teacher.Tno
ORDER BY Sno ASC;

DROP VIEW IF EXISTS teacher_grade;
CREATE VIEW teacher_grade
AS
SELECT sapp_teacher.Tno,Tname,sapp_schedulu.Cno_id,Cname,sapp_student.Sno,sapp_student.Sname,Sdept,Sclass,Grade
FROM sapp_teacher,sapp_schedulu,sapp_course,sapp_scores,sapp_student
WHERE sapp_teacher.Tno=sapp_schedulu.Tno_id
AND sapp_schedulu.Cno_id=sapp_course.Cno
AND sapp_course.Cno=sapp_scores.Cno_id
And sapp_scores.Sno_id=sapp_student.Sno;


-- 重新运行Django ORM
USE StudentManager;
DELETE FROM django_migrations;
-- 删除测试数据
DELETE FROM sapp_scores;
DELETE FROM sapp_schedulu;
DELETE FROM sapp_studaccount;
DELETE FROM sapp_teacaccount;
DELETE FROM sapp_course;
DELETE FROM sapp_teacher;
DELETE FROM sapp_student;
