from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sapp.models import Student, StudAccount
from sapp.db_view import StudentGradeTable
from sapp.form_model import StudentInfoMF, StudentLoginMF


# 首页
def student_home(request):
    return render(request, 'student/stu_home.html')


# 查询成绩
def student_find(request):
    # 处理成绩表
    def data_treating(sc_sheet, label_len: int) -> list:
        grade_sheet = []
        tmp_dt = {}
        for line in sc_sheet:
            tmp_dt[line['Sno']] = tmp_dt.get(line['Sno'], []) + [line]
        for k, v in tmp_dt.items():
            tmp_li = [line['Grade'] for line in v][:label_len]
            tmp_li += [0] * (label_len - len(tmp_li))
            tmp_li.append(sum(tmp_li))
            tmp_li.insert(0, v[0]['Sname'])
            tmp_li.insert(0, k)
            grade_sheet.append(tmp_li)
        grade_sheet.sort(key=lambda x: x[-1], reverse=True)
        for i in range(len(grade_sheet)):
            grade_sheet[i].append(i + 1)
        grade_sheet.sort(key=lambda x: x[0])
        return grade_sheet

    sid = request.session.get('account_cookie')['account']
    the_student_name = Student.objects.filter(Sno=sid).values('Sname')[0]['Sname']
    the_student_sc = StudentGradeTable.objects.filter(Sno=sid)
    stu_clas = the_student_sc[0].Sclass
    all_stu_sc = StudentGradeTable.objects.filter(Sclass=stu_clas).values('Sno', 'Sname', 'Cname', 'Grade')
    cse_name = [course['Cname'] for course in the_student_sc.values()]
    cse_len = len(cse_name)
    scores_label = ['学号', '姓名'] + cse_name + ['总分', '排名']
    scores_sheet = data_treating(all_stu_sc, label_len=cse_len)
    content_data = {
        'the_stu_name': the_student_name,
        'the_stu_sc': the_student_sc,
        'stu_clas': stu_clas,
        'slabel': scores_label,
        'ssheet': scores_sheet
    }
    return render(request, 'student/stu_find.html', content_data)


# 成绩分析
def student_analysis(request):
    sid = request.session.get('account_cookie')['account']
    sname = Student.objects.filter(Sno=sid).values('Sname')[0]['Sname']
    return render(request, 'student/stu_analysis.html', {'sno': sid, 'sname': sname})


# 个人主页
def student_info(request):
    sid = request.session.get('account_cookie')['account']
    stu_info = Student.objects.filter(Sno=sid).first()
    info_form = StudentInfoMF()
    acount_form = StudentLoginMF()
    res_data = {
        'stu_info': stu_info,
        'info_form': info_form,
        'acount_form': acount_form
    }
    return render(request, 'student/stu_info.html', res_data)


# 更新学生信息
@csrf_exempt
def update_student_info(request):
    old_data = Student.objects.filter(Sno=request.POST['Sno']).first()
    form_data = StudentInfoMF(data=request.POST, instance=old_data)
    if form_data.is_valid():
        form_data.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form_data.errors})


# 更新学生密码
@csrf_exempt
def update_student_pwd(request):
    post_data = request.POST
    old_data = StudAccount.objects.filter(Saccount_id=post_data['Saccount']).first()
    form_data = StudentLoginMF(data=post_data, instance=old_data)

    if form_data.is_valid():
        new_data = form_data.cleaned_data
        if new_data['Spwd'] != old_data.Spwd:
            form_data.add_error("Spwd", "原密码错误")
            return JsonResponse({'status': False, 'error': form_data.errors})
        if new_data['new_pwd'] != new_data['again_pwd']:
            form_data.add_error("again_pwd", "与新密码不一致")
            return JsonResponse({'status': False, 'error': form_data.errors})
        if new_data['new_pwd'] == old_data.Spwd:
            form_data.add_error('new_pwd', '与原密码相同，重新改一个吧')
            return JsonResponse({'status': False, 'error': form_data.errors})
        StudAccount.objects.filter(Saccount_id=post_data['Saccount']).update(Spwd=new_data['again_pwd'])
        obj = JsonResponse({'status': True})
        request.session.clear()
        # obj.delete_cookie("account")
        # del request.session['account_cookie']
        return obj
    return JsonResponse({'status': False, 'error': form_data.errors})


# Get Data Tools
class GetDataTools:
    def __init__(self, student_id):
        self.the_student_id = StudentGradeTable.objects.filter(Sno=student_id)
        self.the_stu_sc = self.the_student_id.values('Sno', 'Sname', 'Cname', 'Grade')
        stu_clas = self.the_student_id[0].Sclass
        self.all_stu_sc = StudentGradeTable.objects.filter(Sclass=stu_clas).values('Cname', 'Grade')
        self.cse_name = [course['Cname'] for course in self.the_student_id.values()]
        self.sc_dt = {}
        for stu_line in self.all_stu_sc:
            self.sc_dt[stu_line['Cname']] = self.sc_dt.get(stu_line['Cname'], []) + [stu_line['Grade']]

    def bar_data(self) -> dict:  # 柱状图数据
        data = {
            'x_axis_data': self.cse_name,
            'series_data': [
                {
                    'name': f'{self.the_stu_sc[0]["Sname"]}的成绩',
                    'type': 'bar',
                    'data': [v['Grade'] for v in self.the_stu_sc]
                },
                {
                    'name': '班级平均分',
                    'type': 'bar',
                    'data': [round(sum(v) / len(v), 1) for v in self.sc_dt.values()]
                }]
        }
        return data

    def pie_data(self) -> list:  # 饼图数据
        data = [
            {'value': k['Grade'], 'name': k['Cname']} for k in self.the_stu_sc
        ]
        return data

    def radar_data(self) -> dict:  # 雷达图数据
        data = {
            'indicator_data': [
                {'name': course, 'max': 100} for course in self.cse_name
            ],
            'series_data': [
                {
                    'value': [v['Grade'] for v in self.the_stu_sc],
                    'name': f'{self.the_stu_sc[0]["Sname"]}的成绩',
                    'areaStyle': {
                        'color': 'rgba(74,110,255,0.4)'
                    }
                },
                {
                    'value': [round(sum(v) / len(v), 1) for v in self.sc_dt.values()],
                    'name': '班级平均分',
                    'areaStyle': {
                        'color': 'rgba(106,255,106,0.4)'
                    }
                }
            ]
        }
        return data

    def plot_data(self) -> dict:
        max_sc, min_sc = [], []
        for _, v in self.sc_dt.items():
            max_sc.append(max(v))
            min_sc.append(min(v))
        data = {
            'x_axis_data': self.cse_name,
            'max_sc': max_sc,
            'the_stu_sc': [v['Grade'] for v in self.the_stu_sc],
            'min_sc': min_sc
        }
        return data


# 成绩分析 get 数据
def get_exam_results(request):
    sid = request.session.get('account_cookie')['account']
    gdt = GetDataTools(sid)
    chart_name = request.GET['cn']
    result_data = {
        "status": True,
        "data": {} or []
    }
    if chart_name == 'bar':
        result_data['data'] = gdt.bar_data()
    elif chart_name == 'pie':
        pie_data = gdt.pie_data()
        pie_data.sort(key=lambda x: x['value'])
        result_data['data'] = pie_data
    elif chart_name == 'radar':
        result_data['data'] = gdt.radar_data()
    elif chart_name == 'plot':
        result_data['data'] = gdt.plot_data()
    else:
        result_data['data'] = 'null'
    return JsonResponse(result_data)
