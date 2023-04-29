#For Paginator 
from django.core.paginator import Paginator #import Paginator
# for search query
from django.db.models import Q

# Class based API from https://www.geeksforgeeks.org/class-based-views-django-rest-framework/
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .serializers import UserSerializers

#from django.shortcuts import render
#sudhir Test
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from datetime import datetime
from .models import auth,profile,skills
from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage


import smtplib, ssl
import secrets

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "iot4server@gmail.com"  # Enter your address
receiver_email = "b4sudhir@gmail.com"  # Enter receiver address
password = "qmedqwnyzktkznbu"
message = """\
Subject: Freelancer Project Verification Mail

Hi user,

This is a Verification mail from Freelancer Proejct. Kindly Verify your Credentials by clicking on below given link.
Link : https://scloud.tk/token/"""
context = ssl.create_default_context()

# Create your views here.



def home(request):
    template = loader.get_template('homepage.html')
    if 'login_name' in request.session:
        context = {
                'islogin': True,
                'name' : request.session['login_name'],
                'email' : request.session['login_email']
                }
    else:
       context = {
                    'islogin': False
                 }     
    return render(request,'homepage.html',context)

@csrf_exempt
def signupdata(request):
    submitted = True # flag for submission
    email_verified = False
    data_verified = False
    squery = request.POST
    send_message = "Signup Successfully and Check your email id :"+ squery["signup_email"] +"for verification."
    token = secrets.token_hex(16)
    email_message = message  +  str(token)
    #print(squery)
    if(len(squery["signup_name"])<5 and 
       len(squery["signup_email"])<5 and
       len(squery["signup_number"])!=10 and
       len(squery["signup_password"])<5):
            submitted = False
            send_message = "Something went wrong. Please Fill form properly"
    if submitted :
        try:
            try:
                 if auth.objects.filter(email=squery["signup_email"]).exists():
                     send_message = "Email is already register. Kindly Login with same Email Id"
                 else :
                    authquery = auth(
                        name = squery["signup_name"],
                        email = squery["signup_email"],
                        phone = int(squery["signup_number"]),
                        password = squery["signup_password"],
                        freelancer = bool(squery["freelancer"]),
                        created_date = datetime.now(),
                        verified = 0, 
                        token = token,
                    )
                    data_verified = True
            except:
                send_message ="Something went wrong. Please Fill form properly"
        except:
             send_message ="Something went wrong. Please Fill form properly"
             data_verified = False
        if data_verified:
            try:
                receiver_email = squery["signup_email"]
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, email_message)
                print(email_message)
                email_verified = True                
            except:
                send_message = "Something went wrong. Please check your email."
                email_verified = False 
        if email_verified :
             authquery = auth(
                        name = squery["signup_name"],
                        email = squery["signup_email"],
                        phone = int(squery["signup_number"]),
                        password = squery["signup_password"],
                        freelancer = bool(squery["freelancer"]),
                        created_date = datetime.now(),
                        verified = 0, 
                        token = token,
                    )
             authquery.save()
             send_message = "Signup Successfully and Check your email id :"+ squery["signup_email"] +"for verification."
    return HttpResponse(send_message)

@csrf_exempt
def login(request):
    lq = request.POST
    # print(lq)
    loggedinemail = lq['login_email']
    if auth.objects.filter(email=lq['login_email'],password=lq['login_password']).exists():
        loginquery = auth.objects.filter(email=lq['login_email']).values()
        if(loginquery[0].get('verified')):
            l_detail= auth.objects.filter(email=loggedinemail).values('name')
            request.session['login_email'] = loggedinemail
            print(l_detail)
            login_name = l_detail[0].get('name')
            request.session['login_name']=login_name
            context = {
                    'islogin': True,
                    'name' : request.session['login_name'],
                    'email' : request.session['login_email']
                    }         
            return render(request,'homepage.html',context)
        else:
            return HttpResponse("2")
    else:
        return HttpResponse("1")


def tokenverify(request,token):
    try:
        if auth.objects.filter(token=token).exists():
            if auth.objects.filter(token=token,verified=False).exists():
                auth.objects.filter(token=token).update(verified  =True)
                return HttpResponse("Successfully Verified .. Go to Home Page for login <a href = ""https://scloud.tk""> Freelancer</a>")
            else:
                return HttpResponse("Already Verified... Go to Home Page <a href = ""https://scloud.tk""> Scloud</a>")
        else:
            return HttpResponse("Not Verified .. Go to Home Page and Signup <a href = ""https://scloud.tk""> Scloud</a>")
    except:
        return HttpResponse("Error in Verification.. Go to Home Page and Signup <a href = ""https://scloud.tk""> Scloud</a>")
    
def logout(request):
    if "login_name" in request.session :
        del request.session["login_email"]
        del request.session["login_name"]
        request.session.modified = True
    
    context = {
                'islogin': False
                }
    return redirect("https://scloud.tk")

def profiledisplay(request):
    myauth = auth.objects.filter(email = request.session['login_email']).values()
    myprofile = profile.objects.filter(authTable_id = myauth[0].get('id')).values()
    myskill = skills.objects.filter(authTable_id = myauth[0].get('id')).values()
    message = ""
    messageon = False
    if 'messagetext' in request.session:
        message = request.session['messagetext']
        print("message: ",message)
        del request.session['messagetext']
        messageon = True

    context = {
                'islogin': True,
                'name' : request.session['login_name'],
                'email' : request.session['login_email'],
                'myauthdata':myauth,
                'myprofiledata' : myprofile,
                'myskilldata':myskill,
                'messagetext':message,
                'message':messageon,
                }
    return render(request,'profile.html',context)

def imgupload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        myauth = auth.objects.filter(email = request.session['login_email']).values()
        myprofile = profile.objects.filter(authTable_id = myauth[0].get('id')).values()
        profiles= profile(photo = file_url, authTable_id = myauth[0].get('id'))
        profiles.save()
        return redirect ("/profile")
    return render(request, 'profile.html')

def profiledata(request):
    message = ""
    if request.method == 'GET':
        squery = request.GET
        print(squery['name'])
        
        try:
            if(len(squery['cpwd']) > 0):
                myauth = auth.objects.filter(email = request.session['login_email']).values()
                c_pwd = myauth[0].get('password')
                if(squery['cpwd'] == c_pwd):
                    if(squery['npwd'] == squery['ncpwd']):
                        auth.objects.filter(email = request.session['login_email']).update(password=squery['npwd'])
                        if(len(squery['name'])>5):
                            auth.objects.filter(email = request.session['login_email']).update(name=squery['name'])
                        else :
                            message = "Error in Name"
                        
                        if(len(squery['phone'])==10):
                            auth.objects.filter(email = request.session['login_email']).update(phone=squery['phone'])
                        else :
                            message = "Error in Phone"
                        
                        if(len(squery['address'])>0):
                            profile.objects.filter(authTable_id = myauth[0].get('id')).update(address=squery['address'])
                        else :
                            message = "Error in Address"
                        
                        if(len(squery['aboutme'])>0):
                            profile.objects.filter(authTable_id = myauth[0].get('id')).update(aboutMe=squery['aboutme'])
                        else :
                            message = "Error in AboutMe"
                        
                          #skill data handling
                        myskill = skills.objects.filter(authTable_id = myauth[0].get('id')).values_list('skill', flat=True)    #value list will display only value from skill column in set 
                        #Addition of skill
                        queryskill = request.GET.getlist('skill')
                        for nskill in queryskill:
                                if(len(nskill)>0):
                                    #Addition of skill
                                    if nskill not in myskill:
                                        print("new skill found :", nskill)
                                        mynewskill = skills(
                                                                authTable_id = myauth[0].get('id'),
                                                                skill = nskill
                                        )
                                        mynewskill.save()
                                    else:
                                        print("no new skill found")
                        #deleteion of skill
                        for dskill in myskill:
                            if dskill not in queryskill:
                                skills.objects.filter(authTable_id = myauth[0].get('id'),skill = dskill).delete()
                                print("deleted :",dskill )
                                
                        message ="data saved with new password kindly login with new password"
                    else:
                        message = "new password and confirm new password not matched"
            else:
                        myauth = auth.objects.filter(email = request.session['login_email']).values()
                        if(len(squery['name'])>5):
                            auth.objects.filter(email = request.session['login_email']).update(name=squery['name'])
                        else :
                            message = "Error in Name"
                        
                        if(len(squery['phone'])==10):
                            auth.objects.filter(email = request.session['login_email']).update(phone=squery['phone'])
                        else :
                            message = "Error in Phone"
                        
                        if(len(squery['address'])>0):
                            profile.objects.filter(authTable_id = myauth[0].get('id')).update(address=squery['address'])
                        else :
                            message = "Error in Address"
                        
                        if(len(request.GET.get('devlopertag'))>0):
                            profile.objects.filter(authTable_id = myauth[0].get('id')).update(devlopertag=request.GET.get('devlopertag'))
                        else :
                            message = "Error in devlopertag"
                        
                        if(len(squery['aboutme'])>0):
                            profile.objects.filter(authTable_id = myauth[0].get('id')).update(aboutMe=squery['aboutme'])
                        else :
                            message = "Error in AboutMe"
                        
                        #skill data handling
                        myskill = skills.objects.filter(authTable_id = myauth[0].get('id')).values_list('skill', flat=True)    #value list will display only value from skill column in set 
                        #Addition of skill
                        queryskill = request.GET.getlist('skill')
                        for nskill in queryskill:
                                if(len(nskill)>0):
                                    #Addition of skill
                                    if nskill not in myskill:
                                        print("new skill found :", nskill)
                                        mynewskill = skills(
                                                                authTable_id = myauth[0].get('id'),
                                                                skill = nskill
                                        )
                                        mynewskill.save()
                                    else:
                                        print("no new skill found")
                        #deleteion of skill
                        for dskill in myskill:
                            if dskill not in queryskill:
                                skills.objects.filter(authTable_id = myauth[0].get('id'),skill = dskill).delete()
                                print("deleted :",dskill )
                        
                        #final message
                        message ="data saved !!! No Changes in your Password."
        except Exception as e:
            message = "Error : " and str(e)

    request.session['messagetext'] = message
    return redirect("/profile")

#API Class 
class UserList(APIView):
    def get(self, request, format=None):
        Users = auth.objects.all()
        serializer = UserSerializers(Users, many=True)
        return Response(serializer.data)

def search(request):
    search_post = request.GET.get('search')
    context = {
        
    }
    return render(request, "search.html",context)
def profilecard(request):
    myauth = auth.objects.filter(email = request.session['login_email']).values()
    myprofile = profile.objects.filter(authTable_id = myauth[0].get('id')).values()
    myskill = skills.objects.filter(authTable_id = myauth[0].get('id')).values()
    message = ""
    messageon = False
    if 'messagetext' in request.session:
        message = request.session['messagetext']
        print("message: ",message)
        del request.session['messagetext']
        messageon = True

    context = {
                'islogin': True,
                'name' : request.session['login_name'],
                'email' : request.session['login_email'],
                'myauthdata':myauth,
                'myprofiledata' : myprofile,
                'myskilldata':myskill,
                }
    return render(request, "profilecard.html",context)
