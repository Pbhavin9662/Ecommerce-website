from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView,ListView, CreateView, UpdateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from .forms import *
from django.contrib import messages 
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.http import JsonResponse
import json
from .models import *
from .task import *



def searchView(request):
    query = request.GET['querydata']
    products = Product.objects.filter(description__icontains=query)
    context = {'products':products}
    return render(request, "shop/search.html",context)


class HomeView(TemplateView):
    template_name = 'shop/home.html'

        
    def get(self, request):
        if request.user.is_authenticated:
            
            user=request.user
            account = request.session.get('email')
            print("-----",account)
            ac= Account.objects.get(email=account)
            context={}
            context["products"] =Product.objects.all()[:20]
            context['user']=user
            context["profiles"],created = Profile.objects.get_or_create(account=user)          
            context["ShippingAddress"] ,created = ShippingAddress.objects.get_or_create(account=user)          
            context["BillingAddress"],created = BillingAddress.objects.get_or_create(account=user)          
            order, created = Order.objects.get_or_create(account=user, complete=False)
            context['cartItems'] = order.get_cart_items
            return render(request, "shop/home.html",context)   
        else:
            return render(request, "shop/home.html")
    

 
@method_decorator(login_required,name='dispatch')
class SingleProduct(TemplateView):
        template_name = 'shop/single-product.html'
           
        def get(self, request,pk):
            context={}
            account = request.session.get('email')
            user= Account.objects.get(email=account)
            profiles = Profile.objects.get(account=user.id)
            products = Product.objects.get(id=pk)
            order, created = Order.objects.get_or_create(account=user.id, complete=False)
            cartItems = order.get_cart_items
            related_product = Product.objects.filter(category=products.category)
            context = {'pd': products,'profiles': profiles,'related_product':related_product,'cartItems':cartItems}
            return render(request, self.template_name,context)   


@method_decorator(login_required,name='dispatch')
class shopCategory(ListView):
        template_name = 'shop/category.html'

        def get(self, request):
            account = request.session.get('email')
            ac= Account.objects.get(email=account)
            order, created = Order.objects.get_or_create(account=ac.id, complete=False)
            cartItems = order.get_cart_items
            cats = Category.objects.all()
            brand = Brand.objects.all()
            products = Product.objects.all()
            a = None
            b = None
            subcat_id = request.GET.get('category')
            subcategory_id = request.GET.get('subcategory')
            
            if subcat_id:
                a = SubCategory.get_all_SubCategory_By_Categoryid(subcat_id)
            
            elif subcategory_id:
                b = Product.get_all_product_by_Subcategory(subcategory_id)
                
            context = {'cats': cats, 'brand': brand, 'products': products, 'a': a, 'b': b, 'subcat_id': subcat_id,'cartItems':cartItems}
            return render(request, self.template_name, context)




class RegisterView(TemplateView):
    template_name = 'shop/register.html'

    def post(self, request):
        context={}
        if request.POST:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                account = authenticate(email=email, password=password)
                key=0
                request.session['key']=key
                print("---------register---",account)
                # login(request, account)
                return redirect('login')
            else:
                context['registration_form'] = form
        
        return render(request, self.template_name, context)



    def get(self, request):
        context={}
        form = RegistrationForm()
        context['registration_form'] = form
        return render(request, self.template_name, context)




           

@login_required()
def logout_view(request):
    logout(request)
    return redirect('home')



class LoginView(TemplateView):
    template_name = 'shop/login.html'

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect("home")
        if request.POST:
            form = LoginForm(request.POST)
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)    
                request.session['email'] = email
                
                if user:
                    login(request, user)
                    return redirect("home")
        return render(request,self.template_name)
    def get(self, request):
        context={}
        form = LoginForm()
        context['login_form'] = form
        return render(request, self.template_name, context)

        



@login_required()
def basic(request):
    user = request.session.get('email')
    ac = Account.objects.get(email=user)
    profiles = Profile.objects.get(account=ac.id)
    item = OrderItem.objects.all().count()
    id = profiles.id
    context = {'profiles': profiles,'cartItems':item,'id':id}
    return render(request, "shop/basic.html", context)
       
 

@method_decorator(login_required,name='dispatch')
class profile_view(TemplateView):
    template_name="shop/profile.html"
    def get(self, request):
        account = request.session.get('email')
        user= Account.objects.get(email=account)
        profiles = Profile.objects.get(account=user.id)
        form = ProfileForm(instance=profiles)                 
        context = {'profiles':profiles,'form':form}
        return render(request, self.template_name, context)
    
    
    def post(self, request):
        account = request.session.get('email')
        user= Account.objects.get(email=account)
        profiles = Profile.objects.get(account=user.id)
        form = ProfileForm(request.POST,request.FILES,instance=profiles)
        if form.is_valid():
            form.save()
        context = {'form':form}
        return render(request, self.template_name, context)

   




@login_required()
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(account=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("item was added", safe=False)




@login_required
def cart_view(request):
    if request.user.is_authenticated:
        user =request.user
        account = request.session.get('email')
        ac= Account.objects.get(email=account)
        profiles = Profile.objects.get(account=ac.id)            
        
        order, created = Order.objects.get_or_create(account=user, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        carttotal = order.get_cart_total
        cart = carttotal + (carttotal * 0.18)
        if request.method=="POST":
            sbill = ShippingAddress.objects.get(account=ac.id)
            form = ShippingForm(request.POST,instance=sbill)
            if form.is_valid():
                form.save()
                success = "Shipping Address Successfully add..."
                context = {'success':success,'form':form}
        else:
            sbill = ShippingAddress.objects.get(account=ac.id)
            form = ShippingForm(instance=sbill)

    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'address': 0}
        cartItems = order['get_cart_items']
        carttotal = order['get_cart_total']
        cart = carttotal + (carttotal * 0.18)
        # address = Profile['address']  
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'tax_total': cart,'form':form,'profiles':profiles}
    return render(request, "shop/cart.html", context)



@method_decorator(login_required,name='dispatch')
class checkoutView(View):
    template_name="shop/checkout.html"

    def get(self,request):
        success=None
        account = request.session.get('email')
        ac= Account.objects.get(email=account)
        blObject=BillingAddress.objects.get(account=ac.id)
        profiles= Profile.objects.get(account=ac.id)            
            
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(account=ac.id, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            if blObject:
                form = BillingAddressForm(instance=blObject)
            else:
                form = BillingAddressForm()
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'form': 0}
        context = {'items': items, 'order': order, 'form': form, 'success': success,'profiles':profiles,'cartItems':cartItems}
        return render(request,self.template_name, context)

    def post(self,request):
        account = request.session.get('email')
        user= Account.objects.get(email=account)
        bill = BillingAddress.objects.get(account=user.id)
        BillForm = BillingAddressForm(request.POST,instance=bill)
        if BillForm.is_valid():
            BillForm.save()
            success = "Billing Address Successfully created..."
        context = {'success':success,}
        return render(request,self.template_name, context)
    
    
@method_decorator(login_required,name='dispatch')       
class confirmation(View):
    template_name="shop/confirmation.html"

    def get(self,request):
        account = request.session.get('email')
        ac= Account.objects.get(email=account)
        sp= ShippingAddress.objects.get(account=ac.id)
        bl= BillingAddress.objects.get(account=ac.id)
        profiles = Profile.objects.get(account=ac.id)            
        
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(account=ac.id, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            carttotal = order.get_cart_total
            cart = carttotal + (carttotal * 0.18)
            order_info = Order.objects.get(account=ac.id)
            shipingaddress = ShippingAddress.objects.get(account=ac.id)
            billingaddress = BillingAddress.objects.get(account=ac.id)
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'address': 0, 'billingaddress': 0, 'shipingaddress': 0}
            cartItems = order['get_cart_items']
            carttotal = order['get_cart_total']
            cart = carttotal + (carttotal * 0.18)
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipingaddress': shipingaddress,
                'billingaddress': billingaddress, 'carttotal': cart, 'o': order_info,'profiles':profiles}

        return render(request,self.template_name, context)





   
    
# for generating pdf invoice
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.core.mail import EmailMultiAlternatives

@login_required()
def render_to_pdf(request):
    account = request.session.get('email')
    ac= Account.objects.get(email=account)
        
    if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(account=ac.id, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
            carttotal = order.get_cart_total
            cart = carttotal + (carttotal * 0.18)
            order_info = Order.objects.get(account=ac.id)
            shipingaddress = ShippingAddress.objects.get(account=ac.id)
            billingaddress = BillingAddress.objects.get(account=ac.id)
    else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'address': 0, 'billingaddress': 0, 'shipingaddress': 0}
            cartItems = order['get_cart_items']
            carttotal = order['get_cart_total']
            cart = carttotal + (carttotal * 0.18)
            context = {'items': items, 'order': order, 'cartItems': cartItems, 'shipingaddress': shipingaddress,
                'billingaddress': billingaddress, 'carttotal': cart, 'o': order_info,'profiles':profiles}
    template = get_template('shop/confirmation.html')
    data= {'items': items, 'order': order, 'cartItems': cartItems, 'shipingaddress': shipingaddress,
                'billingaddress': billingaddress, 'carttotal': cart, 'o': order_info}
    html  = template.render(data)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    filename = 'Invoice_'  + '.pdf'
    mail_subject = 'Recent Shopping Order Details'    
    template = get_template('shop/emailinvoice.html')
    context_dict={'user':request.user,'message':'invoice send'}
    message  = template.render(context_dict)
    to_email = account
    send_mail_task(mail_subject,to_email,message,filename,pdf)
    
    if request.method=="POST":
        orderdata = Order.objects.get(account=ac.id)
        orderdata.delete()
        print("------cart data is deleted------")
        return HttpResponse("<h1>you have successful complete your trasaction thankyou</h2><a href="">Home</a>")
    
    return render(request, 'shop/success.html', context_dict)



