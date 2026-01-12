from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from mainapp.models import Book
from decimal import Decimal
import requests

# Create your views here.
from django.http import HttpResponse

def add_to_cart(request, id):
    return HttpResponse(f"Book with ID {id} added to cart.")


def index(request):
  context= {
    'userid' : request.session.get('userid'),
    'books' : Book.objects.all(),
    'new_arrivals' : Book.objects.all()[:10],
  } 
  return render(request, 'index.html', context)

def about(request):
  return render(request, 'about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save enquiry to DB
        enq = Enquiry(name=name, contactno=contactno, email=email, subject=subject, message=message)
        enq.save()

        # Send SMS
        url = "http://sms.bulkssms.com/submitsms.jsp"
        params = {
            "user": "BRIJESH",
            "key": "066c862acdXX",
            "mobile": contactno,
            "message": "Thanks for enquiry we will contact you soon.\n\n-Bulk SMS",
            "senderid": "UPDSMS",
            "accusage": "1",
            "entityid": "1201159543060917386",
            "tempid": "1207169476099469445"
        }

        try:
            response = requests.get(url, params=params)
            print("SMS Response:", response.text)
        except Exception as e:
            print("SMS Sending Failed:", e)

        # Success message
        messages.success(request, "Your enquiry has been submitted successfully.")

        # You can also use redirect if needed
        # return redirect('contact')  

    # Always render with context, even if empty
    return render(request, 'contact.html', {})

    
    
def login(request):
  if request.method =='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
      user = LoginInfo.objects.get(usertype="user",username=username ,password=password)
      if user is not None:
        request.session['userid'] = username
        messages.success(request,"Welcome User")
        return redirect('index')
        
    except LoginInfo.DoesNotExist:
      messages.error(request,"Invalid username or password")
      return redirect('login')
  return render(request, 'login.html')







def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        password = request.POST.get('password') 
        cpassword = request.POST.get('cpassword') 

        if password != cpassword:
            messages.error(request, "Password and Confirm password do not match")
            return redirect('register') 
            
        if LoginInfo.objects.filter(username=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')
        
        log = LoginInfo(usertype="user", username=email, password=password)
        log.save()

        user = UserInfo(name=name, email=email, contactno=contactno, login=log)
        user.save()

        messages.success(request, "Registration is done Successfully.")
        return redirect('register')

    return render(request, 'register.html')
    
def profile(request):
    return render(request, 'profile.html')
    
    
    
def adminlogin(request):
    
    if request.method =='POST':
        username= request.POST.get('username')
        password= request.POST.get('password')
        
        try:
            ad = LoginInfo.objects.get(username = username, password = password)
            if ad is not None:
              request.session['adminid']=username
              messages.success(request, "Welcome Admin")
              return redirect('admindash')
        except LoginInfo.DoesNotExist:
            messages.error(request,",Invalid User or password")
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')
    
def book_details(request, id):
  context={
    'userid' : request.session.get('userid'),
    'book' : Book.objects.get(id=id)
    }
  return render(request, 'book_details.html',context)
  


def test(request):
    return render(request, 'test.html')
    
  