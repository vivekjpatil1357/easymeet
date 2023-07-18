from django.db import models

# Create your models here.


class users(models.Model):
    username = models.CharField(primary_key=True, max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    email = models.EmailField(max_length=254, default='')
    date = models.DateField(auto_now=True)
    isactive = models.CharField(max_length=100,default='',blank=True)

class history(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE)
    meet_name=models.CharField(max_length=30,default='')
    date=models.DateField(auto_now=True)
    join_time=models.TimeField(null=True)
    leave_time=models.TimeField(null=True)
    total_time=models.CharField(default='',max_length=10)

