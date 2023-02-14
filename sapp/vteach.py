from django.shortcuts import render

from sapp.db_view import TeacherGrade


# 首页
def thome(request):
    return render(request, 'teacher/t_home.html')


# 查询
def tfind(request):
    uid = request.session.get('account_cookie')['account']
    grade_info = TeacherGrade.objects.filter(Tno=uid).values()
    for line in grade_info:
        print(line)
    return render(request, 'teacher/t_find.html')
