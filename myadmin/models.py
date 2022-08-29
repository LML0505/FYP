import hashlib
from django.db import models
from datetime import datetime
from static.yolox.predict import pred
# Create your models here.


#company
class Company(models.Model):
    name = models.CharField(max_length=50,default='c')#company name 
    status = models.IntegerField(default=1)        #status:1active /9delete 
    create_at = models.DateTimeField(default=datetime.now)    #create time 
    update_at = models.DateTimeField(default=datetime.now)    #edit time 
    
  

    class Meta:
        db_table = "company"  #
       
#account model 
class Account(models.Model):
    company_id =models.IntegerField() # 0 means is personal account/ other means the accout belongs to company
    company_name = models.CharField(max_length=45,default='')
    nickname = models.CharField(max_length=45)    #nickname
    account = models.CharField(max_length=45)    #account
    password_hash = models.CharField(max_length=100)#password_hashed by MD5 
    password_salt = models.CharField(max_length=100)    #passwordsalt for MD5
    status = models.IntegerField(default=1)    #status:1 farmer /2 corp science /3 dataanalyst/4 manager/8 suspended/ 9deleted/0 is root account 
    create_at = models.DateTimeField(default=datetime.now)    #createtime
    update_at = models.DateTimeField(default=datetime.now)    #changetime

    def toDict(self):
       return {'id':self.id,'company_id':self.company_id,'company_name':self.company_name,'nickname':self.nickname,'account':self.account,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    def setUserStatus(self,status):
            self.status=status
            self.save()
            return self.status
        
    def validateLogin(self,username,password):
       result=0
       if self.account==username:
            md5 = hashlib.md5()
                    #password + salt 
            s = password+str(self.password_salt)
            md5.update(s.encode('utf-8'))# put the md5 inside
                        #make compare with the password_hash in database
            if self.password_hash == md5.hexdigest():
                result = 1

       return result 

    def ifadmin(self):
        if 1<self.status<8:
            return 1
        else:
            return 0
    def ifstaff(self):
        if 0<self.status<8:
            return 1
        else:
            return 0
    class Meta:
        db_table = "account"  # 更改表名

class Picture(models.Model):
    submit_pic=models.CharField(max_length=100)    #pic
    user_id=models.IntegerField() # user_id
    user_name=models.CharField(max_length=45)
    company_id =models.IntegerField() # which company, personal or company 
    company_name=models.CharField(max_length=45)
    predict_pic=models.CharField(max_length=100)    #pic after predict
    count_result =models.IntegerField()# count_result 
    label=models.CharField(max_length=45)
    comment=models.CharField(max_length=100)
    create_at = models.DateTimeField(default=datetime.now) #update time 
    status =models.IntegerField(default=1) # 1 activate, 0 delete  

    def toDict(self):
           return {'submit_pic':self.submit_pic,'user_id':self.user_id,'user_name':self.user_name,'company_id':self.company_id,'company_name':self.company_name,'predict_pic':self.predict_pic,
           'count_result':self.count_result,'status':self.status,'label':self.label,'comment':self.comment,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S')}
    
    def dosubmitpic(self):
         self.submit_pic='1658831715.063401.jpg'
         self.user_id= 1
         self.user_name= 'test'
         self.company_id=0
         self.company_name='company'
         self.predict_pic='predict'
         self.count_result=66
         self.label='farm1'
         self.comment='nocomment'
         self.create_at=datetime.now()
         self.status=1
                   
                
   
        
    class Meta:
            db_table = "picture"  # 更改表名

