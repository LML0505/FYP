"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from myadmin.views import index,account,company,history

urlpatterns = [
    path('', index.index,name="myadmin_index"),

    #company_info 
    path('company/<int:pIndex>', company.index, name="myadmin_company_index"),
    #path('category/load/<int:sid>', category.loadCategory, name="myadmin_company_load"),
    path('company/add', company.add, name="myadmin_company_add"),
    path('company/insert', company.insert, name="myadmin_company_insert"),
    path('company/del/<int:cid>', company.delete, name="myadmin_company_del"),
    path('company/edit/<int:cid>', company.edit, name="myadmin_company_edit"),
    path('company/update/<int:cid>', company.update, name="myadmin_company_update"),

    #user_account info 
    path('account/<int:pIndex>', account.index, name="myadmin_user_index"),#view
    path('account/add',account.add,name="myadmin_user_add"), #to add
    path('account/insert',account.insert,name="myadmin_user_insert"), #do add
    path('account/del/<int:uid>',account.delete,name="myadmin_user_del"), #delete
    path('account/edit/<int:uid>',account.edit,name="myadmin_user_edit"), #to edit
    path('account/update<int:uid>',account.update,name="myadmin_user_update"), #do edit

    # login 
    path('login', index.login, name="myadmin_login"),
    path('dologin', index.dologin, name="myadmin_dologin"),
    path('logout', index.logout, name="myadmin_logout"),
    path('verify', index.verify, name="myadmin_verify"), #验证码 

    #picture 
    path('history/<int:pIndex>',history.index,name="myadmin_uhistory"),
    path('history/del/<int:pid>', history.delete, name="myadmin_history_del"),
    


]
