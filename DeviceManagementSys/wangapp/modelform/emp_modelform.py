from django import forms
from wangapp import models
from  django.core.exceptions import ValidationError

class EmployeeModelForm(forms.ModelForm):
    class Meta:
        model = models.Employee
        fields = ['name','password','job','phone_number','institution','power']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

class LoginForm(forms.Form):
    name=forms.CharField(label="用户名",widget=forms.TextInput,required=True)
    password=forms.CharField(label="密码",widget=forms.PasswordInput,required=True)
    name.widget.attrs = {'class': 'form-control'}
    password.widget.attrs = {'class': 'form-control'}