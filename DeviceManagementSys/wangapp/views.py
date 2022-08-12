import datetime
import json
from django.http import JsonResponse

from django.shortcuts import render,redirect

# Create your views here.
from wangapp import models
from wangapp.utils.pageination import Pageination
from wangapp.modelform.device_modelform import DeviceAddModelForm,DeviceApplyModelForm,DeviceApplyModelForm2
from  wangapp.modelform.emp_modelform import LoginForm



# def powerJudge(request):
#     powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
#     if powerJudeg <= 1:
#         return redirect('/emp/selflist/')






#设备列表

def device_list(request):
    # print("type ", models.Device.objects.filter().values('type').distinct())
    # typeInfo = models.Device.objects.filter().values('type').distinct()
    # # legend数据  设备种类  横轴
    # legend = []
    # for i in range(len(typeInfo)):
    #     legend.append(typeInfo[i]['type'])
    # print("legend", legend)
    #
    # # xdata_list  legend 机构名  图例
    # institutionInfo = models.Employee.objects.filter().values('institution').distinct()
    # xdata_list = []
    # for i in range(len(institutionInfo)):
    #     xdata_list.append(institutionInfo[i]['institution'])
    # print("xdata_list: ", xdata_list)
    #
    # # 数据
    # data_list = []
    #
    # for i in range(len(xdata_list)):
    #     dic={
    #         "institution": xdata_list[i],
    #         "type": 'bar',
    #         "data":[
    #
    #     models.device_applied.objects.filter(institution=xdata_list[i]).filter(type=legend[j]).count() for j in range(len(legend))
    #
    #
    #         ]
    #
    #     }
    #
    #
    #     data_list.append(dic)
    # print(data_list)









    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    data_dict={}
    search_value=request.GET.get('q',"")
    if search_value:
        data_dict["type__contains"]=search_value
    queryset=models.Device.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context={
        'queryset':page_queryset,
        'search_value':search_value,
        'page_string':page_string

    }
    return render(request,'device_list.html',context)

#添加设备
def device_add(request):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    if request.method=='GET':
        form = DeviceAddModelForm()
        return render(request, 'device_add.html', {'form': form})
    form=DeviceAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        print(request.session['info']['user_name'] )
        return redirect('/device/list/')
    return render(request,'device_add.html',{'form':form})

#已申请设备（待修改）
def device_applied(request):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    if powerJudeg==2:
        institution_name = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0][
            'institution']
        queryset = models.device_applied.objects.filter(institution=institution_name)
    else:
        queryset = models.device_applied.objects.filter(state=2)

    # data_dict={}
    # search_value=2
    # data_dict["state__contains"]=search_value
    # queryset=models.device_applied.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context={
        'queryset':page_queryset,
        'page_string':page_string
    }
    return render(request,'device_applied.html',context)

#空闲设备查看
def device_free(request):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')


    data_dict={}
    search_value=0
    data_dict["state__contains"]=search_value
    queryset=models.Device.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context={
        'queryset':page_queryset,
        'page_string':page_string

    }
    return render(request,'device_free.html',context)



#设备申请
def device_apply(request,nid):
    # s: {'id': 1, 'name': 'wyz', 'password': '123456789', 'job': 'admin', 'phone_number': '12345678909',
    #     'institution': 'dggonghang', 'power': 3}
    # s: {'id': 3, 'deviceSeq': 'printer123123', 'type': 'printer', 'purchaseTime': datetime.date(2022, 8, 6), 'state': 0}
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    mo=models.device_apply()

    mo.deviceID=models.Device.objects.filter(id=nid).first()
    personInfo = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]
    deviceInfo=models.Device.objects.filter(id=nid).values()[0]
    mo.applyPersonID=models.Employee.objects.filter(id=personInfo['id']).first()
    mo.applyPersonName=personInfo['name']
    mo.deviceSeq=deviceInfo['deviceSeq']
    mo.type=deviceInfo['type']
    mo.purchaseTime=deviceInfo['purchaseTime']
    mo.applyTime=datetime.datetime.now()
    mo.institution=personInfo['institution']

    s=models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]
    p=models.Device.objects.filter(id=nid).values()[0]
    print("s: ",p)
    row_object=models.Device.objects.filter(id=nid).first()
    if request.method=="GET":
        form = DeviceApplyModelForm(instance=row_object)
        return render(request,'device_apply.html',{'form':form})
    form=DeviceApplyModelForm(instance=row_object,data=request.POST)
    print("POST : ",request.POST.get("reason"))
    if form.is_valid():

        form.save()

        ## 修改借出状态
        mo.reason=request.POST.get("reason")

        models.Device.objects.filter(id=nid).update(state=1)
        mo.state=models.Device.objects.filter(id=nid).values()[0]['state']
        mo.save()

        return redirect('/device/list/')
    context = {
        'form': form
    }
    return render(request,'device_apply.html',context)

def device_applying(request):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')


    data_dict = {}
    search_value = 1
    data_dict["state__contains"] = search_value
    queryset = models.device_apply.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'page_string': page_string

    }
    return render(request, 'device_applying.html', context)

# 审批中取消

# models.Device.objects.filter(id=nid).update(state=0)
#     models.device_apply.objects.filter(id=nid).delete()

def applying_cancel(request,nid):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    speReason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['reason']
    if speReason == "报障或到期":
        mo = models.device_applied()
        mo.deviceID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id']
        mo.applyPersonID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0][
            'applyPersonID_id']
        mo.applyPersonName = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values(
            'applyPersonName')
        mo.deviceSeq = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('deviceSeq')
        mo.type = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('type')
        mo.purchaseTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('purchaseTime')
        mo.applyTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('applyTime')
        mo.institution = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('institution')
        mo.reason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('reason')
        mo.state = 2
        mo.save()
        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
            state=2)
    else:
        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
            state=0)

    models.device_apply.objects.filter(id=nid).delete()
    return redirect('/device/applying/')

#审批信息
def applyinfo_list(request):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')


    data_dict = {}
    search_value = 1
    # data_dict["state__contains"] = search_value
    if powerJudeg==2:
        institution_name = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0][
            'institution']
        queryset = models.device_apply.objects.filter(institution=institution_name)
    else:
        queryset = models.device_apply.objects.filter(state=search_value)


    # institution_name = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['institution']

    print(queryset,1)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'page_string': page_string

    }
    return render(request, 'applyinfo_list.html', context)

def applyinfo_confirm(request,nid):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')


    models.Device.objects.filter(deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
        lastState=2)
    models.Device.objects.filter(deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(state=2)
    allInfo=models.device_apply.objects.filter(id=nid).values()[0]
    print(allInfo)
    ##如果包含“报障或到期”
    speReason=models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['reason']
    print("speRea: ",speReason)
    if speReason=="报障或到期":
        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(state=0)
        models.device_apply.objects.filter(id=nid).delete()
        return redirect('/applyinfo/list/')

    print("sed: ",models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id'])
    mo=models.device_applied()
    mo.deviceID_id=models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id']
    mo.applyPersonID_id=models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['applyPersonID_id']
    mo.applyPersonName = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('applyPersonName')
    mo.deviceSeq = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('deviceSeq')
    mo.type = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('type')
    mo.purchaseTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('purchaseTime')
    mo.applyTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('applyTime')
    mo.institution = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('institution')
    mo.reason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('reason')
    mo.state = models.Device.objects.filter(deviceSeq=allInfo['deviceSeq']).values('state')

    mo.save()



    models.device_apply.objects.filter(id=nid).delete()
    return redirect('/applyinfo/list/')

def applyinfo_reject(request,nid):
    powerJudeg = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]['power']
    if powerJudeg <= 1:
        return redirect('/emp/selflist/')

    allInfo = models.device_apply.objects.filter(id=nid).values()[0]
    print(allInfo)
    ##如果包含“报障或到期”
    speReason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['reason']
    print("speRea: ", speReason)
    if speReason == "报障或到期":
        mo = models.device_applied()
        mo.deviceID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id']
        mo.applyPersonID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0][
            'applyPersonID_id']
        mo.applyPersonName = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values(
            'applyPersonName')
        mo.deviceSeq = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('deviceSeq')
        mo.type = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('type')
        mo.purchaseTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('purchaseTime')
        mo.applyTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('applyTime')
        mo.institution = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('institution')
        mo.reason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('reason')
        mo.state = 2
        mo.save()

        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
            state=2)
        models.device_apply.objects.filter(id=nid).delete()

        return redirect('/applyinfo/list/')
    else:
        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
            state=0)

    models.device_apply.objects.filter(id=nid).delete()
    return redirect('/applyinfo/list/')

def device_sta(request):
    return render(request,'draw.html')

def device_bar(request):
    print("type ", models.Device.objects.filter().values('type').distinct())
    typeInfo = models.Device.objects.filter().values('type').distinct()
    # legend数据  设备种类  横轴
    legend = []
    for i in range(len(typeInfo)):
        legend.append(typeInfo[i]['type'])
    print("legend", legend)

    # data_list  legend 机构名  图例
    institutionInfo=models.Employee.objects.filter().values('institution').distinct()
    xdata_list=[]
    for i in range(len(institutionInfo)):
        xdata_list.append(institutionInfo[i]['institution'])
    print("xdata_list: ",xdata_list)


    # 数据
    data_list=[]

    for i in range(len(xdata_list)):

        dic={"name":xdata_list[i],
             "type":'bar',
             "data":[
                 models.device_applied.objects.filter(institution=xdata_list[i]).filter(type=legend[j]).count() for j in range(len(legend))
             ]
             }
        data_list.append(dic)

    result = {
        "status": True,
        "data": {
            'legend': xdata_list,
            'series': data_list,
            'xAxis': legend,

        }
    }
    print(result)

    return JsonResponse(result)




# 普通员工
def emp_list(request):
    data_dict = {}
    search_value = request.GET.get('q', "")
    if search_value:
        data_dict["type__contains"] = search_value
    queryset = models.Device.objects.filter(**data_dict)
    print("que: ",queryset.values())
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'search_value': search_value,
        'page_string': page_string

    }
    return render(request, 'emp_list.html', context)

def emp_applying(request):
    data_dict = {}
    search_value = request.session['info']['user_name']
    print("search_value: ",search_value)
    data_dict["applyPersonName__contains"] = search_value
    queryset = models.device_apply.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'page_string': page_string

    }
    return render(request, 'emp_applying.html', context)

def emp_applying_cancel(request,nid):
    allInfo = models.device_apply.objects.filter(id=nid).values()[0]
    speReason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['reason']

    if speReason == "报障或到期":
        mo = models.device_applied()
        mo.deviceID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id']
        mo.applyPersonID_id = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0][
            'applyPersonID_id']
        mo.applyPersonName = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values(
            'applyPersonName')
        mo.deviceSeq = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('deviceSeq')
        mo.type = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('type')
        mo.purchaseTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('purchaseTime')
        mo.applyTime = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('applyTime')
        mo.institution = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('institution')
        mo.reason = models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values('reason')
        mo.state = 2
        mo.save()
        models.Device.objects.filter(
                deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
                state=2)
    else:
        models.Device.objects.filter(
            deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
            state=0)

    models.device_apply.objects.filter(id=nid).delete()
    return redirect('/emp/applying/')






    # lastNum=models.device_apply.objects.filter(id=nid).values()[0]['lastState']
    # print(lastNum)
    # if lastNum==2:
    #     models.Device.objects.filter(
    #         deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
    #         state=2)
    # else:
    #     models.Device.objects.filter(
    #         deviceSeq=models.device_apply.objects.filter(id=nid).values()[0]['deviceSeq']).update(
    #         state=0)
    #     models.device_apply.objects.filter(id=nid).update(lastState=0)
    #
    #
    #
    #
    #
    #
    #
    # # models.device_apply.objects.filter(id=nid).update(state=0)
    # models.device_apply.objects.filter(id=nid).delete()
    #
    # return redirect('/emp/applying/')


def emp_applied(request):
    data_dict = {}
    search_value = request.session['info']['user_name']
    print("search_value: ", search_value)
    data_dict["applyPersonName__contains"] = search_value
    queryset = models.device_applied.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'page_string': page_string

    }
    return render(request, 'emp_applied.html', context)

def emp_free(request):
    data_dict = {}
    search_value = 0
    data_dict["state__contains"] = search_value
    queryset = models.Device.objects.filter(**data_dict)
    page_object = Pageination(request, queryset)
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    context = {
        'queryset': page_queryset,
        'page_string': page_string

    }
    return render(request, 'emp_free.html', context)

def emp_apply(request,nid):
    mo = models.device_apply()

    mo.deviceID = models.Device.objects.filter(id=nid).first()
    personInfo = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]
    deviceInfo = models.Device.objects.filter(id=nid).values()[0]
    mo.applyPersonID = models.Employee.objects.filter(id=personInfo['id']).first()
    mo.applyPersonName = personInfo['name']
    mo.deviceSeq = deviceInfo['deviceSeq']
    mo.type = deviceInfo['type']
    mo.purchaseTime = deviceInfo['purchaseTime']
    mo.applyTime = datetime.datetime.now()
    mo.institution = personInfo['institution']

    s = models.Employee.objects.filter(name=request.session['info']['user_name']).values()[0]
    p = models.Device.objects.filter(id=nid).values()[0]
    print("s: ", p)
    row_object = models.Device.objects.filter(id=nid).first()
    if request.method == "GET":
        form = DeviceApplyModelForm(instance=row_object)
        return render(request, 'emp_apply.html', {'form': form})
    form = DeviceApplyModelForm(instance=row_object, data=request.POST)
    print("POST : ", request.POST.get("reason"))
    if form.is_valid():
        form.save()

        ## 修改借出状态
        mo.reason = request.POST.get("reason")

        models.Device.objects.filter(id=nid).update(state=1)
        mo.state = models.Device.objects.filter(id=nid).values()[0]['state']
        mo.save()

        return redirect('/emp/selflist/')
    context = {
        'form': form
    }

    return render(request, 'emp_apply.html', context)


#gai gaigai
def emp_applying_change(request,nid):
    models.Device.objects.filter(deviceSeq=models.device_applied.objects.filter(id=nid).values()[0]['deviceSeq']).update(
        state=1)
    allInfo = models.device_applied.objects.filter(id=nid).values()[0]
    print(allInfo)
    # print("sed: ", models.device_apply.objects.filter(deviceSeq=allInfo['deviceSeq']).values()[0]['deviceID_id'])
    mo = models.device_apply()
    tired=models.device_applied.objects.filter(deviceSeq=allInfo['deviceSeq'])

    mo.deviceID_id = tired.values()[0]['deviceID_id']
    mo.applyPersonID_id = tired.values()[0][ 'applyPersonID_id']
    mo.applyPersonName = tired.values('applyPersonName')
    mo.deviceSeq = tired.values('deviceSeq')
    mo.type = tired.values('type')
    mo.purchaseTime = tired.values('purchaseTime')
    mo.applyTime = tired.values('applyTime')
    mo.institution = tired.values('institution')
    mo.reason = "报障或到期"
    mo.state = 1
    mo.lastState=2
    mo.save()


    # models.device_apply.objects.filter(id=nid).update(state=0)
    models.device_applied.objects.filter(id=nid).delete()

    return redirect('/emp/applying/')






























def login_page(request):
    if request.method=='GET':
        form=LoginForm()
        return render(request, 'login_page.html',{'form':form})
    form=LoginForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data)
        # emp_object=models.FreeEmployee.objects.filter(**form.cleaned_data).first()
        emp_object=models.Employee.objects.filter(**form.cleaned_data).first()
        if not emp_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login_page.html', {'form': form})
        request.session['info'] = {'user_name': emp_object.name, 'user_password': emp_object.password}
        print(models.Employee.objects.filter(power=emp_object.power).values()[0]['power'])
        if models.Employee.objects.filter(power=emp_object.power).values()[0]['power']==1:
            return redirect('/emp/selflist/')
        return redirect('/device/list/')







    return render(request,'login_page.html',{'form':form})

def logout(request):
    request.session.clear()
    return redirect('/login/')

