from django.db import models
from datetime import datetime

# Create your models here.
class User(models.Model):
    # 用户名 varchar=20
    username=models.CharField(max_length=20,db_column='user_name')
    # 密码 varchar=100
    password=models.CharField(max_length=100)
    # 真实姓名 varchar=20
    truename=models.CharField(max_length=20,db_column='true_name',null=True)
    # 邮箱  varchar=30
    email=models.CharField(max_length=30)
    # 电话 varchar=20
    phone=models.CharField(max_length=20,null=True)
    # 是否有效 varchar=4
    is_valid=models.IntegerField(max_length=4,default=1)
    # 创建时间
    create_date=models.DateField(default=datetime.now())
    # 修改时间
    update_date=models.DateField(null=True)
    # 激活码  varchar=255
    code =models.CharField(max_length=255,null=True)
    # 状态  varchar=1
    status=models.BooleanField(max_length=1)
    # 时间戳  varchar=255
    timestamp=models.CharField(max_length=255,null=True)


    # 元信息
    class Meta(object):
        db_table='t_user'