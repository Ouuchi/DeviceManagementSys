from django.db import models

# Create your models here.

class Device(models.Model):
    # deviceID=models.IntegerField(verbose_name='设备号',max_length=7)
    deviceSeq=models.CharField(verbose_name='序列号',max_length=32)
    type=models.CharField(verbose_name='设备类型',max_length=16)
    purchaseTime=models.DateField(verbose_name="设备购买时间")

    state_choice=(
        (0,'闲置'),
        (1,'审批中'),
        (2,'已借出')
    )
    state=models.SmallIntegerField(verbose_name="设备状态",choices=state_choice,default=0)
    lastState = models.SmallIntegerField(verbose_name="上一个状态", default=0)
    def __str__(self):
        return str(self.id)


class Employee(models.Model):
    name=models.CharField(verbose_name="姓名",max_length=32)
    password=models.CharField(verbose_name="密码",max_length=32,default=None)
    job=models.CharField(verbose_name="职称",max_length=32)
    phone_number=models.CharField(verbose_name="手机号码",max_length=11)
    institution=models.CharField(verbose_name="所属支行",max_length=64)
    state_choice = (
        (0, '普通'),
        (1, '负责人'),
        (2,'管理员')
    )
    power= models.SmallIntegerField(verbose_name="权限", choices=state_choice, default=0)
    def __str__(self):
        return str(self.id)


class device_apply(models.Model):
    # deviceID=models.IntegerField(verbose_name='设备ID')
    deviceID = models.ForeignKey(verbose_name="设备ID", to='Device', to_field='id', null=True, blank=True,
                                    on_delete=models.SET_NULL, default=None)
    # applyPersonID=models.IntegerField(verbose_name='申请人ID')
    applyPersonID = models.ForeignKey(verbose_name="申请人ID", to='Employee', to_field='id', null=True, blank=True,
                                 on_delete=models.SET_NULL, default=None)
    applyPersonName = models.CharField(verbose_name='申请人姓名', max_length=32)
    deviceSeq=models.CharField(verbose_name='序列号',max_length=32)
    type=models.CharField(verbose_name='设备类型',max_length=16)
    purchaseTime=models.DateField(verbose_name="设备购买时间")
    applyTime=models.DateField(auto_now_add=True,verbose_name="申请时间")
    institution=models.CharField(verbose_name="所属机构",max_length=64,default=None)
    reason=models.TextField(verbose_name="理由",default=None)
    state_choice = (
        (0, '闲置'),
        (1, '审批中'),
        (2, '已借出')
    )
    state = models.SmallIntegerField(verbose_name="设备状态", choices=state_choice, default=0)
    lastState=models.SmallIntegerField(verbose_name="上一个状态",  default=0)

class device_applied(models.Model):
    # deviceID=models.IntegerField(verbose_name='设备ID')
    deviceID = models.ForeignKey(verbose_name="设备ID", to='Device', to_field='id', null=True, blank=True,
                                    on_delete=models.SET_NULL, default=None)
    # applyPersonID=models.IntegerField(verbose_name='申请人ID')
    applyPersonID = models.ForeignKey(verbose_name="申请人ID", to='Employee', to_field='id', null=True, blank=True,
                                 on_delete=models.SET_NULL, default=None)
    applyPersonName = models.CharField(verbose_name='申请人姓名', max_length=32)
    deviceSeq=models.CharField(verbose_name='序列号',max_length=32)
    type=models.CharField(verbose_name='设备类型',max_length=16)
    purchaseTime=models.DateField(verbose_name="设备购买时间",default=None)
    applyTime=models.DateField(auto_now_add=True,verbose_name="申请时间")
    institution=models.CharField(verbose_name="所属机构",max_length=64,default=None)
    reason=models.TextField(verbose_name="理由",default=None)
    state_choice = (
        (0, '闲置'),
        (1, '审批中'),
        (2, '已借出')
    )
    state = models.SmallIntegerField(verbose_name="设备状态", choices=state_choice, default=0)
    lastState = models.SmallIntegerField(verbose_name="上一个状态", default=0)

class change_applyinfo(models.Model):
    # deviceID=models.IntegerField(verbose_name='设备ID')
    deviceID = models.ForeignKey(verbose_name="设备ID", to='Device', to_field='id', null=True, blank=True,
                                    on_delete=models.SET_NULL, default=None)
    # applyPersonID=models.IntegerField(verbose_name='申请人ID')
    applyPersonID = models.ForeignKey(verbose_name="申请人ID", to='Employee', to_field='id', null=True, blank=True,
                                 on_delete=models.SET_NULL, default=None)
    applyPersonName = models.CharField(verbose_name='申请人姓名', max_length=32)
    deviceSeq=models.CharField(verbose_name='序列号',max_length=32)
    type=models.CharField(verbose_name='设备类型',max_length=16)
    purchaseTime=models.DateField(verbose_name="设备购买时间",default=None)
    applyTime=models.DateField(auto_now_add=True,verbose_name="申请时间")
    institution=models.CharField(verbose_name="所属机构",max_length=64,default=None)
    reason=models.TextField(verbose_name="理由",default=None)
    state_choice = (
        (0, '闲置'),
        (1, '审批中'),
        (2, '已借出')
    )
    state = models.SmallIntegerField(verbose_name="设备状态", choices=state_choice, default=0)
    lastState = models.SmallIntegerField(verbose_name="上一个状态", default=0)






