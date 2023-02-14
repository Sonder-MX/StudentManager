"""StudentManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf import settings
from django.urls import path, re_path
from django.views.static import serve
from sapp import views, vstud, vteach

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),  # 媒体文件

    # 登录
    path('login/', views.user_login),

    # 学生
    path('shome/', vstud.student_home),
    path('shome/sfind', vstud.student_find),
    path('shome/analysis', vstud.student_analysis),
    path('shome/get_exam_res', vstud.get_exam_results),  # 获取成绩json数据
    path('shome/sinfo', vstud.student_info),
    path('shome/sinfo/update_info/', vstud.update_student_info),  # 更新学生信息
    path('shome/sinfo/update_pwd/', vstud.update_student_pwd),  # 更新密码

    # 教师
    path('thome/', vteach.thome),
    path('thome/tfind', vteach.tfind),

    # 其他
    path('study_hard/', views.go_to_study)
]
