from django import forms
from wangapp import models
from  django.core.exceptions import ValidationError


class DeviceAddModelForm(forms.ModelForm):
    class Meta:
        model=models.Device
        fields=['deviceSeq','type','purchaseTime']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)


        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control'}

    def clean_deviceSeq(self):
        txt_deviceSeq=self.cleaned_data["deviceSeq"]
        exists=models.Device.objects.filter(deviceSeq=txt_deviceSeq).exists()
        if exists:
            raise ValidationError("该设备已存在，存在该序列号")
        return txt_deviceSeq

class DeviceApplyModelForm(forms.ModelForm):
    class Meta:
        model=models.device_apply
        # fields=['id','deviceSeq','type','purchaseTime']
        fields = ['reason']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control'}

    # def clean_deviceSeq(self):
    #     txt_deviceSeq=self.cleaned_data["deviceSeq"]
    #     exists=models.Device.objects.filter(deviceSeq=txt_deviceSeq).exists()
    #     if exists:
    #         raise ValidationError("该设备已存在，存在该序列号")
    #     return txt_deviceSeq

class DeviceApplyModelForm2(forms.ModelForm):
    class Meta:
        model=models.device_apply
        # fields=['id','deviceSeq','type','purchaseTime']
        fields = ['reason']
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs={'class':'form-control'}