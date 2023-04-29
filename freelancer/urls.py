from django.urls import path
from . import views
from django.conf import settings  
from django.conf.urls.static import static 
from rest_framework.urlpatterns import format_suffix_patterns 

urlpatterns = [
    path('',views.home,name="home"),
    path('signupdata',views.signupdata,name='signupdata'),
    path('token/<str:token>/',views.tokenverify,name='tokenverify'),
    path('login',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('profile/',views.profiledisplay,name='profileshow'),
    path("imgupload", views.imgupload, name="imgupload"),
    path("profiledata", views.profiledata, name="profiledata"),
    path("api/", views.UserList.as_view(), name="userList"),
    path("api/<int:id>", views.UserList.as_view(), name="userList"),
    path("profilecard", views.profilecard, name="profilecard"),
    
]
urlpatterns = format_suffix_patterns(urlpatterns)

if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  