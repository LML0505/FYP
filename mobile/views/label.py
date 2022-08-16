from tracemalloc import start
from venv import create
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import date
import datetime
import random
from django.urls import reverse 
from myadmin.models import Account,Picture
from web.views.history import label
from django.db.models import Sum 

def index (request,pIndex=1):
    user=request.session.get('mobileuser',None)
    uid=user['id']
    ac=Account.objects.get(id=uid)
    cid=user['company_id']
    pic = Picture.objects.exclude(label__exact='') # must get the picture are labeled 
    pic=pic.order_by('-create_at')
    
    mywhere=[]
    list = pic.filter(status=1)
    list=list.filter(company_id=cid)
    if ac.status < 2 :
        list=list.filter(user_id=uid)

    # take distinct value in django must with order_by otherwise wont work 
    all_label=list.distinct().values('label').order_by('label')
    print(all_label)
    #sum=0;
    allpic=[]
    for label1 in all_label:
        print(type(label1)) # is a dict type 
        print(label1['label'])# get his value only 
        sum=list.filter(label=label1['label']).aggregate(num=Sum('count_result'))
        print(sum)
        pcdict={"label":"","total":""}
        pcdict["label"]=label1['label']
        pcdict["total"]=sum['num']
        allpic.append(pcdict)
                

    
    # 获取、判断并封装关keyword键搜索
   
    kw = request.GET.get("keyword",None)
    if kw:
       
            new_allpic=[]
            # 查询店铺名称中只要含有关键字就可以
            for pic in allpic: 
                if pic['label'].find(kw)!=-1:
                    new_allpic.append(pic)
            #list = list.filter(create_at__range=[start_date,end_date])
            allpic.clear()
            allpic=new_allpic
            mywhere.append("from_keyword="+kw)
       
            
    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(allpic,8) #以8条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表
    
    print(list2)
    #遍历信息，并获取对应的商铺名称，以shopname名封装


    return render(request,"mobile/label/index.html",{"piclist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere})


def detail(request,lid=' ',pIndex=1):
       
    user=request.session.get('mobileuser',None)
    uid=user['id']
    ac=Account.objects.get(id=uid)
    cid=user['company_id']
    pic = Picture.objects
    pic=pic.order_by('-create_at')
    label=lid 
    mywhere=[]
    list = pic.filter(status=1)
    list=list.filter(company_id=cid)
    list=list.filter(label=lid)
    if ac.status < 2 :
        list=list.filter(user_id=uid)
    
    # 获取、判断并封装关keyword键搜索
    kw1 = request.GET.get("from_keyword",None)
    kw = request.GET.get("keyword",None)
    if kw1:
        if kw:
            # mean from to 
            start_date=datetime.datetime.strptime(kw1,"%Y-%m-%d")
            kw_date=datetime.datetime.strptime(kw,"%Y-%m-%d")
            end_date=(kw_date+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            # 查询店铺名称中只要含有关键字就可以
            list = list.filter(create_at__gte=start_date,create_at__lt=end_date)
            #list = list.filter(create_at__range=[start_date,end_date])
            
            mywhere.append("from_keyword="+kw1)
            mywhere.append("keyword="+kw)
        else: # has from no to 
            start_date=datetime.datetime.strptime(kw1,"%Y-%m-%d")
            #end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            end_str=datetime.datetime.now().strftime("%Y-%m-%d")
                # 查询店铺名称中只要含有关键字就可以
            list = list.filter(create_at__gte=start_date)
                #list = list.filter(create_at__range=[start_date,end_date])
        
            mywhere.append("from_keyword="+kw1)
            #mywhere.append("end_time="+end_str)
    else:
        if kw: # only to 
            #timestamp = 1528797322
            #date_time = datetime.fromtimestamp(timestamp)
            #str_start=date_time.strftime("%Y-%m-%d")
            kw_date=datetime.datetime.strptime(kw,"%Y-%m-%d")
            # add one more day so will include the end_date
            end_date=(kw_date+datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            
            # 查询店铺名称中只要含有关键字就可以
            list = list.filter(create_at__lt=end_date)
            #list = list.filter(create_at__range=[start_date,end_date])
                
            #mywhere.append('start'+str_start)
            mywhere.append("keyword="+kw)
            


    

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,8) #以8条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #遍历信息，并获取对应的商铺名称，以shopname名封装


    return render(request,"mobile/label/detail.html",{"label":label,"piclist":list2,'plist':plist,'pdex':pIndex,'maxpages':maxpages,'mywhere':mywhere})


def delete(request,lid=0):    
    try:
        user=request.session.get('webuser',None)
        uid=user['id']
        ac=Account.objects.get(id=uid)
        cid=user['company_id']
        pic = Picture.objects
        pic=pic.order_by('-create_at')
        label=lid 
        mywhere=[]
        list = pic.filter(status=1)
        list=list.filter(company_id=cid)
        list=list.filter(label=lid)
        if ac.status < 2 :
            list=list.filter(user_id=uid)
       
        for ob in list :
            ob.status=0 #means delete 
            ob.save()
       # ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        context={"info":"delete success ！"}
    except Exception as err:
        print(err)
        #context={"info":"delete fail !"}

    return redirect('/mobile/label/1')

def detail_delete(request,pid=0):
       
    try:
        ob = Picture.objects.get(id=pid)
        ob.status = 0
       # ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        #context={"info":"delete success ！"}
    except Exception as err:
        print(err)
        #context={"info":"delete fail !"}

    return redirect('/mobile/label/1')


def label(request,pid=0):
       
    #try:
        ob = Picture.objects.get(id=pid)
        context={'obj':ob}
        return render(request,"mobile/label/label.html",context)

def dolabel(request,pid=0):
       
    try:
        ob = Picture.objects.get(id=pid)
        label=request.POST.get('label',None)
        comment=request.POST.get('comment',None)
        ob.label=label 
        ob.comment=comment
       # ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"label success ！"}
    except Exception as err:
        print(err)
        context={"info":"label fail !"}

    return redirect('/mobile/label/1')
