
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
    
    try:
        #picture upload or single or mutiple 
        myfile = request.FILES.getlist("cover_pic",None)
        if not myfile:
            return HttpResponse("no pic upload")
        piclist=[]
        for file in myfile:      # write document   
            cover_pic=str(time.time())+"."+file.name.split('.').pop()
            piclist.append(cover_pic)
            destination = open("./static/uploads/picture/"+cover_pic,"wb+")
            for chunk in file.chunks():      # write document
              destination.write(chunk)  
            destination.close()
        context={"pic":cover_pic}
    except Exception as err:
        print(err)
      
 
    allpic=[]
  
    for cover_pic in piclist:
        mode = ''
        if cover_pic.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            mode = 'predict'
            # return 
            img_pre, num = pred(mode, cover_pic)
           
            pcdict={"pic":"","pre":"","num":""}
            pcdict["pic"]=cover_pic
            pcdict["pre"]=img_pre
            pcdict["num"]=num 

           
            allpic.append(pcdict)
            
            op=Picture()
            op.submit_pic=cover_pic
            wuser=request.session.get('webuser',None)
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
    
    #print(piclist)
    #print(allpic)

                           
    return render(request, "web/mupload/mshowpic.html", {"piclist": piclist , "allpic":allpic})
