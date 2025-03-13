
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from MakeupApp.models import Cart, Customer, Menu, Parlour
from django.contrib import messages  

from MakeupApp.forms import ParForm,MenuForm
from MakeupProject import settings

# Create your views here.
def index(request):
    return render(request,'MakeupApp/index.html')

def sign_in(request):
    return render(request,'MakeupApp/sign_in.html')

def sign_up(request):
    return render(request,'MakeupApp/sign_up.html')

def handle_signin(request):
    li = Parlour.objects.all()
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:  # ✅ Now inside the POST block
            cus = Customer.objects.get(username=username, password=password)
            if username == 'admin':
                return render(request, 'MakeupApp/success.html')
            else:
                return render(request, 'MakeupApp/cusdisplay_par.html', {'username': username, 'li': li})
        except Customer.DoesNotExist:
            return render(request, 'MakeupApp/failed.html')


def handle_signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        try:
            cus = Customer.objects.get( username =  username, password = password)
        except:
            cus = Customer(username= username, password = password, email = email, mobile= mobile, address=address)
            cus.save()
        return render(request, 'MakeupApp/sign_in.html')
    else:
        return HttpResponse('Invalid Request')

def add_par(request):
    form = ParForm(request.POST or None)
    if form.is_valid():
        par_name = request.POST.get('Par_name')
        try: 
            par = Parlour.objects.get(Par_name = par_name)
        except:
            form.save()
            return redirect('MakeupApp:display_par')
    return render(request, 'MakeupApp/add_par.html',{'form':form})

def display_par(request):
    li = Parlour.objects.all()
    return render(request, 'MakeupApp/display_par.html',{'li':li})

def view_menu(request, id):
    par = Parlour.objects.get(pk=id)
    menu = Menu.objects.filter(par=par)  
    return render(request, 'MakeupApp/menu.html',{'par':par, 'menu':menu})

# def add_menu(request, par_id):
#     form = MenuForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('MakeupApp:view_menu', par_id)
#     return render(request,'MakeupApp/menu_form.html',{'form':form})

from django.shortcuts import get_object_or_404

def add_menu(request, par_id):
    parlour = get_object_or_404(Parlour, id=par_id)  # Get the Parlour object

    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu_item = form.save(commit=False)  # Don't save yet
            menu_item.par = parlour  # Assign the Parlour (ForeignKey)
            menu_item.save()  # Now save with correct 'par_id'
            return redirect('MakeupApp:view_menu', par_id)
    else:
        form = MenuForm()

    return render(request, 'MakeupApp/menu_form.html', {'form': form})


def delete_menu(request,id):
    item = Menu.objects.get(pk=id)
    par_id = item.par.id
    item.delete()
    return redirect(request,'MakeupApp:view_menu',par_id)

def cusdisplay_par(request, username):
    customer = Customer.objects.get(username=username)
    li = Parlour.objects.all()
    return render(request, 'MakeupAPp/cusdisplay_par.html',{'li':li, 'username':username})

def cusmenu(request,id, username):
    par = Parlour.objects.get(pk=id)
    menu = Menu.objects.filter(par=par)  
    return render(request, 'MakeupApp/cusmenu.html',{'par':par, 'menu':menu, 'username':username})

def show_cart(request, username):
    customer = Customer.objects.get(username=username)
    cart = Cart.objects.filter(customer= customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    return render(request, 'MakeupApp/show_cart.html', {'items':items, 'total_price':total_price,'username':username})

def add_to_cart(request,username,menuid):
    customer = Customer.objects.get(username = username)
    item = Menu.objects.get(pk=menuid) 
    cart, created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    messages.success(request,f"{item.item_name} added")
    return redirect('MakeupApp:cusmenu', id = item.par.id,username=username)

def checkout(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'MakeupApp/checkout.html',{'error':'Your cart is Empty'})

    import razorpay  # type: ignore # Ensure this is at the top of your file

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


    order_data = {
        'amount':int(total_price * 100),
        'currency':'INR',
        'payment_capture':'1',
    }
    order = client.order.create(data = order_data)
    return render(
        request, 'MakeupApp/checkout.html',
        {'username':username,
        'cart_items':cart_items,
        'total_price':total_price,
        'razorpay_key_id':settings.RAZORPAY_KEY_ID,
        'order_id':order['id'],
        'amount':total_price,
        }
    )

def orders(request, username):
        customer = Customer.objects.get(username = username)
        cart = Cart.objects.filter(customer=customer).first()
        cart_items = cart.items.all() if cart else []
        total_price = cart.total_price() if cart else 0

        if cart:
            cart.items.clear()

        return render(request, 'MakeupApp/orders.html',{
        'username':username,
        'cart_items':cart_items,
        'total_price':total_price,
        'customer':customer
        })

def delete_menu(request,id):
    item = Menu.objects.get(pk=id)
    res_id = item.par.id
    item.delete()
    return redirect('MakeupApp:view_menu',res_id)

def cusdisplay_par(request, username):
    customer = Customer.objects.get(username=username)
    li = Parlour.objects.all()
    return render(request, 'MakeupAPp/cusdisplay_par.html',{'li':li, 'username':username})

def cusmenu(request,id, username):
    par = Parlour.objects.get(pk=id)
    menu = Menu.objects.filter(par=par)  
    return render(request, 'MakeupApp/cusmenu.html',{'par':par, 'menu':menu, 'username':username})

def show_cart(request, username):
    customer = Customer.objects.get(username=username)
    cart = Cart.objects.filter(customer= customer).first()
    items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0
    return render(request, 'MakeupApp/show_cart.html', {'items':items, 'total_price':total_price,'username':username})

def add_to_cart(request,username,menuid):
    customer = Customer.objects.get(username = username)
    item = Menu.objects.get(pk=menuid) 
    cart, created = Cart.objects.get_or_create(customer = customer)
    cart.items.add(item)
    messages.success(request,f"{item.item_name} added")
    return redirect('MakeupApp:cusmenu', id = item.par.id,username=username)

def checkout(request, username):
    customer = Customer.objects.get(username = username)
    cart = Cart.objects.filter(customer = customer).first()
    cart_items = cart.items.all() if cart else []
    total_price = cart.total_price() if cart else 0

    if total_price == 0:
        return render(request, 'MakeupApp/checkout.html',{'error':'Your cart is Empty'})

    import razorpay  # type: ignore # Ensure this is at the top of your file

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


    order_data = {
        'amount':int(total_price * 100),
        'currency':'INR',
        'payment_capture':'1',
    }
    order = client.order.create(data = order_data)
    return render(
        request, 'MakeupApp/checkout.html',
        {'username':username,
        'cart_items':cart_items,
        'total_price':total_price,
        'razorpay_key_id':settings.RAZORPAY_KEY_ID,
        'order_id':order['id'],
        'amount':total_price,
        }
    )

def orders(request, username):
        customer = Customer.objects.get(username = username)
        cart = Cart.objects.filter(customer=customer).first()
        cart_items = cart.items.all() if cart else []
        total_price = cart.total_price() if cart else 0

        if cart:
            cart.items.clear()

        return render(request, 'MakeupApp/orders.html',{
        'username':username,
        'cart_items':cart_items,
        'total_price':total_price,
        'customer':customer
        })