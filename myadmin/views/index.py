from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import random
from myadmin.models import Account





def index(request):
    return render(request,"myadmin/index/index.html")


def login(request):
    return render(request,'myadmin/index/login.html')

# 会员执行登录
def dologin(request):
    #验证判断
    verifycode = request.session['verifycode']
    code = request.POST['code']
   
    if verifycode != code:
        context = {'info':'verificode wrong！'}
        return render(request,"myadmin/index/login.html",context)
    try:
        user=Account.objects.get(account=request.POST['username'])
        #see if is admin
        if user.status == 0:
            # see if password correct    
                import hashlib
                md5 = hashlib.md5()
            #password + salt 
                s = request.POST['pass']+user.password_salt
                md5.update(s.encode('utf-8'))# put the md5 inside
                #make compare with the password_hash in database
                if user.password_hash == md5.hexdigest():
                #login in success 
                    print ('login success')
                    # write into session 
                    request.session['adminuser']=user.toDict()
                    #record = history()
                    #record.account_id = user.id
                    #record.login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #record.logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    #record.save()
                    #request.session['history']=record.toDict()
                    
                    #redirect to admin mgt page 
                    return redirect(reverse("myadmin_index"))
                    
                else :
                    context= {"info":"password is wrong "} 




        else:
           context= {"info":"account is not valid "} 

    except Exception as err:
        print(err)
        context= {"info":"account is not exist "}
    
    return render(request,"myadmin/index/login.html",context)

# 会员退出
def logout(request):
   #pid=request.session['history']['id']
   # print(pid)
   # record = history.objects.filter(id=pid)
   # record.logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #record.save()
    #del request.session['history']
    del request.session['adminuser']
    return redirect(reverse("myadmin_login"))

def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
