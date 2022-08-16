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
from web.views import index,mupload,history,account,label 

urlpatterns = [
    path('index', index.index,name="web_index"),

    path('', index.login, name="web_login"),
    path('dologin', index.dologin, name="web_dologin"),
    path('logout', index.logout, name="web_logout"),
    path('verify', index.verify, name="web_verify"), #验证码 
    path('regis',index.regis,name="web_regis"),
    path('doregis',index.doregis,name="web_doregis"),
    path('manual', index.manual, name="web_manual"),
    path('contact', index.contact, name="web_contact"),

    #path for upload picture 
   # path('upload',upload.addpic,name="web_addpic"),
    #path('doupload',upload.insert,name="web_picture_upload"),
    #path for multiple upload picture 
    path('mupload',mupload.addmpic,name="web_m_addpic"),
    path('domupload',mupload.minsert,name="web_mpicture_upload"),
    #path for upload history
    path('history/<int:pIndex>',history.index,name="web_uhistory"),
    path('history/del/<int:pid>', history.delete, name="web_history_del"),
    path('history/label/<int:pid>', history.label, name="web_history_label"),
    path('history/dolabel/<int:pid>', history.dolabel, name="web_history_dolabel"),
    #path for label history 
    path('label/<int:pIndex>',label.index, name="web_label_index"),
    path('label/detail/<str:lid>/<int:pIndex>',label.detail, name="web_label_detail"),
    path('label/delete/<str:lid>',label.delete, name="web_label_del"),
    path('label/change/<int:pid>', label.label, name="web_label_change"),
    path('label/dolabel/<int:pid>', label.dolabel, name="web_label_dolabel"),
    path('label/del/<int:pid>', label.detail_delete, name="web_label_detail_del"),

  #user_account info 
    path('account/<int:pIndex>', account.index, name="web_user_index"),#view
    path('account/add',account.add,name="web_user_add"), #to add
    path('account/insert',account.insert,name="web_user_insert"), #do add
    path('account/del/<int:uid>',account.delete,name="web_user_del"), #delete
    path('account/edit/<int:uid>',account.edit,name="web_user_edit"), #to edit
    path('account/update<int:uid>',account.update,name="web_user_update"), #do edit
    
]
