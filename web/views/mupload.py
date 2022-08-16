
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
import time,os
from datetime import datetime
from static.yolox.predict import pred
from myadmin.models import Account,Picture 
from sympy import content

def addmpic(request):
    return render(request,"web/mupload/mupload.html")
def minsert(request):
    '''执行添加'''
    try:
        #图片的上传处理
        myfile = request.FILES.getlist("cover_pic",None)
        if not myfile:
            return HttpResponse("no pic upload")
       # cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        piclist=[]
        for file in myfile:      # 分块写入文件  
            cover_pic=str(time.time())+"."+file.name.split('.').pop()
            piclist.append(cover_pic)
            destination = open("./static/uploads/picture/"+cover_pic,"wb+")
            for chunk in file.chunks():      # 分块写入文件  
              destination.write(chunk)  
            destination.close()
        context={"pic":cover_pic}
        #实例化model，封装信息，并执行添加
        '''
        ob = Product()
       
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.cover_pic = cover_pic
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"add success！"}
        '''
    except Exception as err:
        print(err)
        #context={"info":"add fail!"}

    #pred_piclist=[]
    #count=[]
    allpic=[]
    #pcdict={}
    for cover_pic in piclist:
        mode = ''
        if cover_pic.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            mode = 'predict'
            # 返回一个文件名和框数 -- String/Char
            img_pre, num = pred(mode, cover_pic)
           
            pcdict={"pic":"","pre":"","num":""}
            #pcdict.update({"pic": cover_pic}) 
            #pcdict.update({"pre": img_pre}) 
            #pcdict.update({"num": num})
            pcdict["pic"]=cover_pic
            pcdict["pre"]=img_pre
            pcdict["num"]=num 

           
            allpic.append(pcdict)
            
          
            #print(img_pre, num)
            op=Picture()
            op.submit_pic=cover_pic
            wuser=request.session.get('webuser',None)
            #print(wuser)
            op.user_id=wuser['id']
            op.user_name=wuser['account']
            op.company_id=wuser['company_id']
            op.company_name=wuser['company_name']
            op.predict_pic=img_pre
            op.count_result=num 
            op.label=request.POST.get('label',None)
            op.comment=request.POST.get('comment',None)
            op.status = 1
            op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            op.save()
    
    print(piclist)
    print(allpic)

                           
    return render(request, "web/mupload/mshowpic.html", {"piclist": piclist , "allpic":allpic})