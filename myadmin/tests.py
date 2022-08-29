from turtle import update
from django.test import TestCase
import unittest 
from urllib import response
from django.test import SimpleTestCase, TestCase, Client 
from django.urls import reverse, resolve 
from myadmin.models import Account,Picture,Company
from django.core.paginator import Paginator
from datetime import datetime
import random
import hashlib
from static.yolox.predict import pred
# Create your tests here.
'''
class TestEntity_login(TestCase):
        def setUp(self): 
            md5 = hashlib.md5()
            n = random.randint(100000, 999999)
            s = '123456'+str(n) 
            md5.update(s.encode('utf-8'))
            self.account1=Account.objects.create(
                    account='test1',
                    nickname='test1', 
                    company_id=0,
                    company_name='', 
                    password_hash = md5.hexdigest(),
                    password_salt = n, 
                    status=1,           
                )
        def check_account_create_correct(self):
            self.assertEqual(self.account1.account,'test1')
        def test_login_is_correct_account(self):
            self.assertEqual(self.account1.account,'test1')
        def test_login_is_correct_password(self):    
            self.assertEqual(self.account1.validateLogin(self.account1.account,'123456'),1)
        def test_account_status_change(self):    
            self.assertEqual(self.account1.setUserStatus(3),3)

class TestPicture_submit(TestCase):
        def setUp(self): 
          pic=Picture.objects
          pic.dosubmitpic()
        def check_submit(self):
            self.assertEqual(self.submit_pic,'submit')
'''

class TestPicture_num(TestCase):
        def setUp(self): 
           self.pic=Picture.objects
           self.pic.dosubmitpic()
           mode = 'predict'
         
        def check_submit(self):
            self.assertEqual(self.pic.submit_pic,'1658831715.063401.jpg')
        def check_num(self):
            self.assertEqual(pred('predict', self.pic),'1658831715.063401.jpg','26')
       
        def tearDown(self) -> None:
            return super().tearDown()