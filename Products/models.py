
from django.db import models
from django.contrib.auth.models import User
from .storage import OverwriteStorage

class Users(models.Model):  
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    User_Name = models.CharField(max_length=20) 
    Email = models.CharField(max_length=40) 
    Password  = models.CharField(max_length=20)  
      
    def __str__(self):
        return self.User_Name      

class Items(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    photo = models.ImageField(null=True)

    def __str__(self):
        return self.title

class Content(models.Model):
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    description = models.CharField(max_length=10000)
    cost = models.IntegerField()
    specs = models.CharField(max_length=1000,null=True)
    
    def __str__(self):
        return self.item.title

class info(models.Model):
    itemid = models.CharField(max_length=200)
    usern = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.itemid

class Med_file(models.Model):
    filename = models.CharField(max_length=200)
    mediafile = models.FileField(storage=OverwriteStorage())

    def __str__(self):
        return self.filename 
