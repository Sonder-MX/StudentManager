from sapp import models
from django.forms import ModelForm
from django.forms import fields as fls
from django.forms import widgets as wgt


# 学生登录信息
class StudentLoginMF(ModelForm):
    new_pwd = fls.CharField(
        label='新密码',
        widget=wgt.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}),
        max_length=12,
        min_length=6
    )

    again_pwd = fls.CharField(
        label='再次输入',
        widget=wgt.PasswordInput(attrs={'class': 'form-control', 'placeholder': '再次输入新密码'}),
        max_length=12,
        min_length=6
    )

    class Meta:
        model = models.StudAccount
        exclude = ['Saccount']
        widgets = {
            'Spwd': wgt.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入原密码'}),
        }
        error_messages = {
            'new_pwd': {
                'min_length': '请输入6~12位密码'
            },
            'again_pwd': {
                'min_length': '请输入6~12位密码'
            }
        }


# 学生个人信息
class StudentInfoMF(ModelForm):
    class Meta:
        model = models.Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, tag in self.fields.items():
            tag.widget.attrs = {'class': 'form-control', 'placeholder': tag.label}
