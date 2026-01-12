from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import *
from . models import *
import stripe
#from .models import OrderItem, Order
from .models import Cart, CartItems, Order, OrderItem, UserInfo


from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


# Create your views here.
def userdash(request):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  context = {
    'name' : user.name,
    'userid' :userid,
    'profile':user.profile
  }
  return render(request, 'userdash.html', context)
  
  
def viewcart(request):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  ucart =  Cart.objects.filter( user = user).first()
  if ucart is None:
    cart = Cart(user = user)
    cart.save()
  items = CartItems.objects.filter(cart=Cart.objects.filter( user = user).first())
  total = 0
  for i in items:
    total = total + i.get_total_price()
    
  context = {
    'name' : user.name,
    'userid' :userid,
    'profile':user.profile,
    'items':items,
    'total':total
  }
  return render(request, 'viewcart.html', context)
def userlogout(request):
  return render(request, 'userlogout.html', context)
  

from django.shortcuts import get_object_or_404

def addtocart(request,id):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  ucart =  Cart.objects.filter( user = user).first()
  if ucart is None:
    cart = Cart(user = user)
    cart.save()
  if request.method == 'POST':
    quantity = request.POST.get('quantity')
    if  quantity is None:
      quantity = 1
    book = Book.objects.get(id =id)
    ci = CartItems(cart = Cart.objects.filter(user = user).first(), book = book, quantity = quantity)
    ci.save()
    messages.success(request,"Book added to cart")
    return redirect('viewcart')
  else:
    return redirect('index')
    
def removeitem(request,id):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  ucart =  Cart.objects.filter( user = user).first()
  book = Book.objects.get(id=id)
  CartItems.object.filter(cart=ucart,book=book).delete()
  messages.success(request,"Book removed form cart")
  return redirect('viewcart')
  



def checkout(request):
    if 'userid' not in request.session:
        messages.error(request,"You are not logged in")
        return redirect('login')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)
    cart = Cart.objects.get(user=user)
    items = CartItems.objects.filter(cart=cart)

    line_items = []

    for item in items:
        line_items.append({
            'price_data': {
                'currency': 'inr',
                'unit_amount': int(item.book.price * 100),
                'product_data': {
                    'name': item.book.title,
                },
            },
            'quantity': item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card', 'sepa_debit'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/userapp/payment_success/'),
        cancel_url=request.build_absolute_uri('/viewcart/'),
    )

    return redirect(session.url, code=303)


def payment_success(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('login')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)

    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItems.objects.filter(cart=cart)

        if not cart_items.exists():
            messages.warning(request, "No items found in your cart.")
            return redirect('index')

        # Calculate total amount
        total_amount = sum(item.get_total_price() for item in cart_items)

        # Create Order
        order = Order.objects.create(user=user, total_amount=total_amount)

        # Create OrderItems and calculate total_price for each
        order_items_list = []
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
            # Add total_price attribute dynamically
            order_item.total_price = order_item.quantity * order_item.price
            order_items_list.append(order_item)

        # Clear cart
        cart_items.delete()

        # Send confirmation email
        subject = "Order Confirmation"
        msg = f"Dear {user.name},\n\nThank you for your order!\n\nTotal Amount: ₹{total_amount}\n\nBest regards,\nVidya Prakashan Mandir Pvt. Ltd."
        try:
            send_mail(
                subject=subject,
                message=msg,
                from_email='vidyaprakashan@example.com',
                recipient_list=[user.email],
                fail_silently=True
            )
        except:
            messages.warning(request, "Payment successful! Order placed, but email could not be sent.")

        messages.success(request, "Payment successful! Your order has been placed.")
        return render(request,'payment_success.html', {
            'order': order,
            'order_items': order_items_list,
            'total_amount': total_amount
        })

    except Cart.DoesNotExist:
        messages.error(request, "Cart not found.")
        return redirect('index')

        
        
def userorders(request):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  orders = Order.objects.filter(user=user)
  order_items = []
  for o in orders:
    order_items.append(OrderItem.objects.filter(order=o))
  context = {
    'name' : user.name,
    'userid' :userid,
    'profile':user.profile,
    'order_items' : order_items
  }
  return render(request, 'userorders.html', context)



def userprofile(request):
  if not 'userid' in request.session:
    messages.error(request, "You are not logged in")
    return redirect('login')
  userid = request.session.get('userid')
  user = UserInfo.objects.get(email=userid)
  context = {
    'name' : user.name,
    'userid' :userid,
    'profile':user.profile,
    'user' : user
  }
  return render(request, 'userprofile.html', context)
  

def editprofile(request):
    if not 'userid' in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')

    userid = request.session.get('userid')
    user = UserInfo.objects.get(email=userid)

    if request.method == 'POST':
        name = request.POST.get('name')
        contactno = request.POST.get('contactno')
        address = request.POST.get('address')
        profile = request.FILES.get('profile')

        user.name = name
        user.contactno = contactno
        user.address = address
        if profile:
            user.profile = profile
        user.save()
        messages.success(request, "Profile Updated successfully")
        return redirect('userprofile')

    context = {
        'user': user
    }
    return render(request, 'editprofile.html', context)