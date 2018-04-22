from django.forms import fields, widgets
from django import forms
from django.core.exceptions import ValidationError
from blog import models
from django.core.validators import RegexValidator

class RegisterFm(forms.Form):
    username = fields.CharField(max_length=14,
                               min_length=6,
                               error_messages={'required': '用户名不能为空',
                                               'max_length': '长度不能大于14',
                                               'min_length': '用户名长度不能小于6'},
                                widget=widgets.TextInput(attrs={'class': 'form_control', }),
                                label='用户名')

    password = fields.CharField(max_length=14,
                               min_length=6,
                               error_messages={'required': '用户名不能为空',
                                               'max_length': '长度不能大于14',
                                               'min_length': '密码长度不能小于6'},
                                widget=widgets.PasswordInput(attrs={'class': 'form_control', 'placeholder':
                                                                    '密码在6到14个字符之间'}),
                                label='密  码',
                                strip=True,
                                validators=[RegexValidator(r'((?=.*\d))^.{6,14}$', '必须包含数字'),
                                            RegexValidator(r'((?=.*[a-zA-Z]))^.{6,14}$', '必须包含字母'),
                                            RegexValidator(r'^.(\S){6,10}$', '密码不能包含空白字符'),
                                            ]
                                )
    password_again = fields.CharField(max_length=14,
                                min_length=6,
                                error_messages={'required': '用户名不能为空',
                                                'max_length': '长度不能大于14',
                                                'min_length': '密码长度不能小于6'},
                                widget=widgets.PasswordInput(attrs={'class': 'form_control', 'placeholder':
                                    '请再次输入密码'}),
                                label='再次输入密码',
                                strip=True)

    verify = fields.CharField(error_messages={'required': '验证码不能为空'},label = '验证码')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        num = models.UserInfo.objects.filter(username=username).count()
        if num:
            raise ValidationError('用户名已经被注册!')
        return username

    def clean(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password_again')
        if not pwd1 == pwd2:
            raise ValidationError('两次密码输入不匹配')
        return self.cleaned_data


class LoginForms(forms.Form):

    username = fields.CharField(error_messages={'required': '请输入用户名'}, label='用户名',
                                widget=widgets.TextInput(attrs={'placeholder': '输入用户名'}))
    password = fields.CharField(error_messages={'required': '密码不能为空'}, label='密码',
                                widget=widgets.PasswordInput(attrs={'placeholder': '输入您的密码'}))
    verify = fields.CharField(error_messages={'required': '请输入验证码'},
                              widget=widgets.TextInput())


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = models.UserInfo.objects.filter(username=username).first()
        if not user:
            raise ValidationError('用户不存在')
        elif password != user.password:
            raise ValidationError('密码错误!')
        return self.cleaned_data