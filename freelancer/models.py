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
    experiance = models.CharField(null=True, max_length=255)
    aboutMe = models.TextField()

class skills(models.Model):
    authTable = models.ForeignKey(
          auth, 
          on_delete=models.CASCADE)
    skill = models.CharField(max_length=255)

