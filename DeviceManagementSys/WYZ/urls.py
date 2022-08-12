"""WYZ URL Configuration

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

from django.urls import path
from wangapp import views



urlpatterns = [
    path('',views.login_page),

    path('device/list/',views.device_list),
    path('device/add/',views.device_add),
    # 设备申领
    path('device/applied/',views.device_applied),
    path('device/free/',views.device_free),
    path('device/applying/',views.device_applying),
    path('device/<int:nid>/apply/',views.device_apply),
    path('device/<int:nid>/cancel/', views.applying_cancel),

    #审批信息
    path('applyinfo/list/',views.applyinfo_list),
    path('applyinfo/<int:nid>/confirm/', views.applyinfo_confirm),
    path('applyinfo/<int:nid>/reject/', views.applyinfo_reject),

    path('applyinfo/<int:nid>/changeConfirm/', views.applyinfo_reject),



    # 普通员工
    path('emp/selflist/',views.emp_list),
    path('emp/applying/',views.emp_applying),
    path('emp/applied/',views.emp_applied),
    path('emp/free/',views.emp_free),
    path('emp/<int:nid>/apply/',views.emp_apply),
    path('emp/<int:nid>/cancel/', views.emp_applying_cancel),
    path('emp/<int:nid>/change/', views.emp_applying_change),

    #统计
    path('device/statistics/',views.device_sta),
    path('device/bar/',views.device_bar),











    path('login/', views.login_page),
    path('logout/', views.logout),

]
