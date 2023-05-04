from django.db import models

# Create your models here.

class auth(models.Model):
    name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    password = models.CharField(max_length=64)
    freelancer = models.BooleanField()
    created_date = models.DateTimeField(null=True)
    verified = models.BooleanField(null=True)
    token = models.CharField(max_length=65, null = True)
    lastseen = models.DateTimeField(null=True)
    
class profile(models.Model):
    # photo = models.ImageField(upload_to='profile_photo')
    authTable = models.OneToOneField(
           auth, 
           on_delete=models.CASCADE, 
           primary_key=True )
    address = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="profile_pic")
    devlopertag = models.CharField(null=True,max_length=255)
    experience = models.CharField(null=True, max_length=255)
    aboutMe = models.TextField()

class skills(models.Model):
    authTable = models.ForeignKey(
          auth, 
          on_delete=models.CASCADE)
    skill = models.CharField(max_length=255)

class profileproj(models.Model):
    authTable = models.ForeignKey(auth,on_delete=models.CASCADE)
    projName = models.CharField(max_length=64)
    projDisc = models.TextField()
    projTime = models.CharField(max_length=64)
    projLang = models.CharField(max_length=64)

class Message(models.Model):
    authTable = models.ForeignKey(auth,on_delete=models.CASCADE)
    msgid = models.UUIDField()
    msgsub = models.CharField(max_length=255)
    msgbody = models.TextField()
    msgtime = models.DateTimeField()
    msgread = models.BooleanField()
    msgrecipent = models.EmailField(null = True)
    

class Project(models.Model):
    authTable = models.ForeignKey(auth,on_delete=models.CASCADE)
    projectName = models.CharField(max_length=64)
    projectDisc = models.TextField()
    projectTime = models.CharField(max_length=64)
    projectLang = models.CharField(max_length=64)

