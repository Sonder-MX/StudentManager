from django.shortcuts import render, redirect
from sapp.models import StudAccount, TeacAccount


# 用户登录
def user_login(request):
    uname = ''
    user_id = 's'
    button_color = ('rgb(56, 101, 252)', 'rgba(56, 101, 252, 0.4)')  # 活动, 不活动
    error_msg = {
        'account': '',
        'pwd': ''
    }
    if request.method == 'GET':
        return render(request, 'login.html',
                      {'uname': uname, 'user_id': user_id, 'bu_c': button_color, 'error_msg': error_msg})

    uid = request.POST['uid']
    uname = request.POST['uname']
    upwd = request.POST['upassword']
    print(uid)
    if uid == 's':
        user_id = 's'
        student_account = StudAccount.objects.filter(Saccount_id=uname)
        if not student_account:
            error_msg['account'] = '该账号不存在，请检查账号或联系老师！'
            return render(request, 'login.html',
                          {'uname': uname, 'user_id': user_id, 'bu_c': button_color, 'error_msg': error_msg})
        if upwd != student_account.values('Spwd')[0]['Spwd']:
            error_msg['pwd'] = '密码错误'
            return render(request, 'login.html',
                          {'uname': uname, 'user_id': user_id, 'bu_c': button_color, 'error_msg': error_msg})

        # 添加cookie和session
        request.session['account_cookie'] = {'identity_label': user_id, 'account': uname}
        request.session.set_expiry(60 * 60 * 24 * 14)  # session 保存14天
        return redirect('/shome/')

    if uid == 't':
        user_id = 't'
        button_color = button_color[::-1]
        teacher_account = TeacAccount.objects.filter(Taccount=uname)
        if not teacher_account:
            error_msg['account'] = '该账号不存在，请检查账号或联系管理员！'
            return render(request, 'login.html',
                          {'uname': uname, 'user_id': user_id, 'bu_c': button_color, 'error_msg': error_msg})
        if upwd != teacher_account.values('Tpwd')[0]['Tpwd']:
            error_msg['pwd'] = '密码错误'
            return render(request, 'login.html',
                          {'uname': uname, 'user_id': user_id, 'bu_c': button_color, 'error_msg': error_msg})

        # 添加cookie和session
        request.session['account_cookie'] = {'identity_label': user_id, 'account': uname}
        request.session.set_expiry(60 * 60 * 24 * 14)  # session 保存14天
        return redirect('/thome/')


# 好好学习 天天向上
def go_to_study(request):
    return render(request, 'study.html')
