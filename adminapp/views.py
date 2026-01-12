from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from .models import *
from userapp.models import *
from decimal import Decimal
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)

def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin') 
    adminid = request.session.get('adminid')
    context = {
      'adminid' : adminid,
      'user_count' : UserInfo.objects.all().count(),
      'book_count' : Book.objects.all().count(),
      'order_count' : Order.objects.all().count(),
      'category_count' : Category.objects.all().count(),
      'total_revenue' : 0,
      'enquiry_count' : Enquiry.objects.all().count(),
      
      
    }
    return render(request, 'admindash.html', context)  # Render admin dashboard with admin id

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']  # Remove admin session
        messages.success(request, "You have logged out successfully")
        return redirect('adminlogin')
    else:
        messages.error(request, "You are not logged in")
        return redirect('index')
    
def viewenq(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')  # Redirect to admin login if not logged in
    adminid = request.session.get('adminid')
    enqs = Enquiry.objects.all()  # Fetch all enquiries
    return render(request, 'viewenq.html' , {'enqs': enqs,'adminid':adminid})
  
def delenq(request,id):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')  # Redirect to admin login if not logged in
    enqs = Enquiry.objects.get(id=id)  # Fetch all enquiries
    enqs.delete()  # Delete the enquiry
    messages.success(request, "Enquiry deleted successfully")
    return redirect('viewenq')  # Redirect to view enquiries page
  
def adminchangepwd(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin') 
    adminid = request.session.get('adminid') 
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd') 
        newpwd = request.POST.get('newpwd')  
        confirmpwd = request.POST.get('confirmpwd')
        try:
            admin = LoginInfo.objects.get(username=adminid)  # Fetch admin 
            if admin.password != oldpwd:
                messages.error(request, "Old password is incorrect")
                return redirect('adminchangepwd')
            elif newpwd != confirmpwd:
                messages.error(request, "New password and confirm password do not match")
                return redirect('adminchangepwd')
            elif admin.password == newpwd:
                messages.error(request, "New password cannot be the same as old password")
                return redirect('adminchangepwd')
            else:
                admin.password = newpwd  # Update admin password
                admin.save()  # Save changes to the database
                messages.success(request, "Password changed successfully")
                return redirect('admindash')  # Redirect to admin dashboard
        except LoginInfo.DoesNotExist:
            messages.error(request, "something went wrong, please try again")
            return redirect('adminlogin')
    return render(request, 'changepss.html',{'adminid':adminid})  

def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        cat = Category(name=name,description=description)
        cat.save()
        messages.success(request,'Category Added Successfully')
        return redirect('addcat')
    return render(request,'addcat.html')
    
    
def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')
    categories = Category.objects.all()
    
    return render(request, 'viewcat.html', {'categories': categories})


#def viewcat(request):
    #if not 'adminid' in request.session:
       # messages.error(request, "You are not Logged in")
       # return redirect('adminlogin')
   # return render(request,'viewcat.html')

def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')
    cats = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        catid = request.POST.get('category')
        cat = Category.objects.get(id=catid)
        description = request.POST.get('description')
        original_price = Decimal(request.POST.get('original_price'))
        price = Decimal(request.POST.get('price'))
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        cover_image = request.FILES.get('cover_image')
        stock = request.POST.get('stock')
        book = Book(title=title,author=author,category=cat,description=description,original_price=original_price,price=price,published_date=published_date,language=language,cover_image=cover_image,stock=stock)
        book.save()
        messages.success(request,"New Book is added successfully")
        return redirect('addbook')
    return render(request,'addbook.html',{'cats':cats})

def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')
    books = Book.objects.all()
    return render(request,'viewbook.html',{'books':books})
    
    
    
    
    
    
    
    
def view_category(request):
    categories = BookCategory.objects.all()
    return render(request, 'viewcat.html', {'categories': categories})
    
    
    
def adminorders(request):
    if not 'adminid' in request.session:
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin') 
    adminid = request.session.get('adminid')
    context = {
      'adminid' : adminid,
      'orders' : Order.objects.all().order_by('-ordered_at'),
    }
    return render(request, 'adminorders.html', context)  # Render admin dashboard with admin id




def edit_category(request, id):
    if not 'adminid' in request.session:   # Admin login check
        messages.error(request, "You are not Logged in")
        return redirect('adminlogin')

    # Jis category ko edit karna hai, use fetch karo
    category = get_object_or_404(Category, id=id)

    if request.method == 'POST':
        # Form se nayi values lo
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Update karo
        category.name = name
        category.description = description
        category.save()

        messages.success(request, "Category updated successfully!")
        return redirect('viewcat')   # Update ke baad list page pe redirect

    # Agar POST nahi hai to form render karo with existing data
    return render(request, 'editcat.html', {'category': category})

