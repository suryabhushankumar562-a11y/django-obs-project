# adminapp/adminappurls.py

app_name = 'adminapp'
"""
URL configuration for obsproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('register/', views.register,name='register'),
    
    path('login/',views.login,name='login'),
    path('profile/',views.profile,name = 'profile'),
    
    path('adminlogin/', views.adminlogin ,name='adminlogin'),

    
    path('adminapp/',include('adminapp.adminappurls')),
    path('userapp/',include('userapp.userappurls')),
    path('book_details/<id>',views.book_details,name="book_details"),
    
    
    path('addtocart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    
    
    path('test/', views.test ,name='test'),
    
    
    
    
    
    
    
    
    
    
    
    
    path('adminapp/', include('adminapp.adminappurls')),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    



