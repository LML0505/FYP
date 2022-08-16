# myobject/myadmin/views/account.py
# account view file 

from xml.etree.ElementTree import PI
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import random

from myadmin.models import Account,Company
#from myadmin.models import history 
# create your views here 

def index(request,pIndex=1):
    '''浏览信息'''
    umod = Account.objects
    ulist= umod.filter(status__lt = 9) # 9 means delete so dun show 
    

    mywhere=[]
    #get search and find 
    kw=request.GET.get("keyword",None)
    if kw:
        ulist =ulist.filter(Q(account__contains=kw)|Q(company_name__contains=kw))
        mywhere.append('keyword='+kw)
    # 分页 seperate page
    pIndex=int(pIndex)
    page=Paginator(ulist,10) #10data for one page
    maxpages=page.num_pages #max pages 
    #判断越界 pIdenx cannot be <1 or more than maxpages 
    if pIndex > maxpages:
        pIndex=maxpages
    if pIndex<1:
        pIndex=1
    list2 = page.page(pIndex)#get the page data
    plist = page.page_range# get page number
     

    #ulist = User.objects.all() #获取所有信息
    #封装信息加载模板输出
    context = {"userlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
    return render(request,"myadmin/account/index.html",context)

def add(request):
    ''' to add info'''
    oc=Company.objects
    clist = oc.filter(status__lt=9)
    context={"company":clist}

    return render (request,"myadmin/account/add.html",context)

def insert(request):
    ''' do add action  '''
    try:
        ob = Account()
        ob.company_id = request.POST['company_id']
        oc=Company.objects.get(id=request.POST['company_id'])
        ob.company_name=oc.name
        ob.nickname = request.POST['nickname']
        ob.account = request.POST['username']
        
        #获取密码并md5 get passworkd and make md5 for safe
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n) 
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n

        ob.status = 4
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save()
        context={'info':"add success!"}
    except Exception as err:
        context ={'info': "add fail! "}
    return render(request,"myadmin/info.html",context)

''' for add test data 
def addtest(request):
    # do add test
    try:
        for i in range(1,101):
            ob = User()
            ob.username = 'test'+str(i)
            ob.nickname = 'test'+str(i)
            #获取密码并md5 get passworkd and make md5 for safe
            import hashlib
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = '123456'+str(n) 
            md5.update(s.encode('utf-8'))
            ob.password_hash = md5.hexdigest()
            ob.password_salt = n

            ob.status = random.randint(1,3)
            ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ob.save()
        context={'info':"add success!"}
    except Exception as err:
        context ={'info': "add fail! "}
    return render(request,"myadmin/info.html",context)
'''

    
def delete(request,uid=0):
    try:
        ob = Account.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ob.save()
        
        context={'info':"delete success!"}
    except Exception as err:
        context ={'info': "delete fail! "}
    return JsonResponse(context)

def edit(request,uid=0):
    ''' go edit infomation '''
    try:
        ob = Account.objects.get(id=uid)
        context={'user':ob}
        return render(request,"myadmin/account/edit.html",context)
    except Exception as err:
        context ={'info': "fail to find the info need to edit "}
        return render(request,"myadmin/info.html",context)
def update(request,uid=0):
    ''' do edit infomation '''
    try:
        import hashlib
        ob = Account.objects.get(id=uid)
        getnewnic=request.POST.get('nickname',None)
        if getnewnic:
            ob.nickname = getnewnic
        ob.status = request.POST['status']
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        getpass=request.POST.get('password',None)
        if getpass:
            s = getpass+str(n) 
            md5.update(s.encode('utf-8'))
            ob.password_hash = md5.hexdigest()
            ob.password_salt = n
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       
        ob.save()
        
        context={'info':"edit success!"}
    except Exception as err:
        context ={'info': "edit fail! "}
    
    return render(request,"myadmin/info.html",context)

