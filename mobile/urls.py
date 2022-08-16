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
from mobile.views import index,upload,history,label
from web.views.index import verify

urlpatterns = [
    # index and login regis url
    path('index', index.index,name="mobile_index"),
    path('',index.login,name="mobile_login"),
    path('verify', index.verify, name="mobile_verify"),
    path('dologin', index.dologin, name="mobile_dologin"),
    path('logout', index.logout, name="mobile_logout"),
    path('regis',index.regis,name="mobile_regis"),
    path('doregis',index.doregis,name="mobile_doregis"),
   
   # upload and count picture 
    path('upload', upload.upload,name="mobile_upload"),
    path('doupload', upload.doupload,name="mobile_doupload"),
    # history 
    path('history/<int:pIndex>', history.index,name="mobile_history"),
    path('history/del/<int:pid>', history.delete, name="mobile_history_del"),
    path('history/label/<int:pid>', history.label, name="mobile_history_label"),
    path('history/dolabel/<int:pid>', history.dolabel, name="mobile_history_dolabel"),
    #label history 
    path('label/<int:pIndex>',label.index, name="mobile_label_index"),
    path('label/detail/<str:lid>/<int:pIndex>',label.detail, name="mobile_label_detail"),
    path('label/delete/<str:lid>',label.delete, name="mobile_label_del"),
    path('label/change/<int:pid>', label.label, name="mobile_label_change"),
    path('label/dolabel/<int:pid>', label.dolabel, name="mobile_label_dolabel"),
    path('label/del/<int:pid>', label.detail_delete, name="mobile_label_detail_del"),

    
    
]

