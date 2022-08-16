# category view 
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime

from myadmin.models import Company

# 菜品分类信息

def index(request,pIndex=1):
    '''浏览信息'''
    smod = Company.objects
    mywhere=[]
    list = smod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询店铺名称中只要含有关键字就可以
        list = list.filter(name__contains=kw)
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        list = list.filter(status=status)
        mywhere.append("status="+status)

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list,10) #以10条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

  
    #封装信息加载模板输出
    context = {"companylist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/company/index.html",context)

#def loadCategory(request,sid):
#    clist = Company.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
 #   return JsonResponse({'data':list(clist)})

def add(request):
    '''加载添加页面'''
   
    return render(request,"myadmin/company/add.html")

def insert(request):
    '''执行添加'''
    try:
        ob = Company()
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"add success！"}
    except Exception as err:
        print(err)
        context={"info":"add fail "}
    return render(request,"myadmin/info.html",context)

def delete(request,cid):
    '''删除信息'''
    try:
        ob = Company.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"delete success ！"}
    except Exception as err:
        print(err)
        context={"info":"delete fail !"}

    return JsonResponse(context)
    #return render(request,"myadmin/info.html",context)


def edit(request,cid):
    '''加载编辑信息页面'''
    try:
        ob = Company.objects.get(id=cid)
      
        context={"company":ob}
        return render(request,"myadmin/company/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

def update(request,cid):
    '''执行编辑信息'''
    try:
        ob = Company.objects.get(id=cid)
        ob.name = request.POST['name']
        #ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"edit success ！"}
    except Exception as err:
        print(err)
        context={"info":"edit fail !"}
    return render(request,"myadmin/info.html",context)