from django.shortcuts import render,redirect
from ecommerce_app.models import *
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def load_home(request):
    products = ProductModel.objects.all()
    return render(request,"initial_home.html",{"products":products})

@login_required(login_url='userlogin')
def load_home_al(request):
    products = ProductModel.objects.all()
    categorys = CategoryModel.objects.all()
    user=CustomerModel.objects.get(user=request.user.id)

    return render(request,"final_home.html",{"categorys":categorys,"products":products,"user":user})

def load_login(request):
    return render(request,"login.html")

def load_signup(request):
    return render(request,"signup.html")

def usercreate(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        username=request.POST['usrname']
        age=request.POST['age']
        dob=request.POST['dob']
        gender=request.POST['gender']
        address=request.POST['address']
        phno=request.POST['phno']
        email=request.POST['email']
        image=request.FILES.get('file')
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password==cpassword: 
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This Username Already Exists!!!')
                return redirect('load_signup')
            
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                user.save()

                customer = User.objects.get(username=username)
                data = CustomerModel(
                    user_age = age,
                    user_gender = gender,
                    user_dob = dob,
                    user_addr = address,
                    user_phno = phno,
                    photo = image,
                    user=customer)
                data.save()

        else:
            messages.info(request, 'Password Does Not Match!!!')
            return redirect('load_signup')   
        return redirect('load_login')
    else:
        return render(request,'signup.html')
    
@login_required(login_url='userlogin')
def edit_user(request,pk):
    if request.method=='POST':
        user = CustomerModel.objects.get(id=pk)
        user_data = User.objects.get(id=user.user.id)
        user_data.first_name = request.POST.get('fname')
        user_data.last_name = request.POST.get('lname')
        user_data.email = request.POST.get('email')
        user.user_phno = request.POST.get('phno')
        user.user_age = request.POST.get('age')
        user.user_addr = request.POST.get('address')
        old_img=user.photo
        new_img=request.FILES.get('file')
        if old_img !=None and new_img==None:
            user.photo=old_img
        else:
            user.photo=new_img


        user.save()
        user_data.save()
        return redirect("load_home_user_details",user.id)
    return render(request,"load_edit_user.html",user.id)



@login_required(login_url='userlogin')
def load_edit_user(request,pk):
    categorys = CategoryModel.objects.all()
    user=CustomerModel.objects.get(id=pk)
    return render(request,"edit_user.html",{"categorys":categorys,"user":user})


@login_required(login_url='userlogin')
def load_home_user_details(request,pk):
    categorys = CategoryModel.objects.all()
    user=CustomerModel.objects.get(id=pk)
    return render(request,"home_user_details.html",{"categorys":categorys,"user":user})


def userlogin(request):
    if request.method == 'POST':
        username = request.POST['usrname']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            customer = User.objects.get(username=username)
            if customer.is_superuser :
                messages.info(request, f'Welcome {username}')
                return redirect('load_menu')

            else:
                return redirect('load_home_al')
        else:
            messages.info(request, 'Invalid Username or Password. Try Again.')
            return redirect('load_login')
    else:
        return redirect('load_login')

@login_required(login_url='userlogin')
def load_product(request):
    categorys =CategoryModel.objects.all()
    return render(request,'product.html',{"categorys":categorys})

@login_required(login_url='userlogin')
def load_menu(request):
    return render(request,'menu.html')

@login_required(login_url='userlogin')
def productcreate(request):
    if request.method=='POST':
        pr_name=request.POST['pname']
        pr_cost=request.POST['cost']
        pr_discount = request.POST['discount']
        pr_brand = request.POST['brand']
        pr_rating = request.POST['rating']
        pr_colour = request.POST['colour']
        pr_description = request.POST['description']
        manufacture_date = request.POST['mdate']
        pr_mimage = request.FILES.get('mphoto')
        pr_simage1 = request.FILES.get('photo1')
        pr_simage2 = request.FILES.get('photo2')
        pr_simage3 = request.FILES.get('photo3')
        select_item=request.POST['select_item']
        category=CategoryModel.objects.get(id=select_item)
        
        pr_discost = int(pr_cost)-(int(pr_cost)*float(int(pr_discount)/100)) 


        if ProductModel.objects.filter(pr_name=pr_name).exists():
            messages.info(request, 'This Product Already Exits!!!')
            return redirect('load_product')
            
        else:
            data = ProductModel(
                pr_name = pr_name,
                pr_cost = pr_cost,
                pr_discount = pr_discount,
                pr_discost = pr_discost,
                pr_brand = pr_brand,
                pr_rating = pr_rating,
                pr_colour = pr_colour,
                pr_description = pr_description,
                manufacture_date = manufacture_date,
                pr_mimage = pr_mimage,
                pr_simage1 = pr_simage1,
                pr_simage2 = pr_simage2,
                pr_simage3 = pr_simage3,
                category=category)
            data.save()
            messages.info(request, 'Product Added Succesfully')
            return redirect('load_product')   
    else:
        return render(request,'product.html')
    
@login_required(login_url='userlogin')
def edit_product(request,pk):
    if request.method=='POST':
        product = ProductModel.objects.get(id=pk)
        product.pr_name = request.POST.get('pname')
        product.pr_cost = request.POST.get('cost')
        product.pr_discount = request.POST.get('discount')
        product.pr_brand = request.POST.get('brand')
        product.pr_rating = request.POST.get('rating')
        product.pr_colour = request.POST.get('colour')
        product.pr_description = request.POST.get('description')

        old_img=product.pr_mimage
        new_img = request.FILES.get('mphoto')
        if old_img !=None and new_img==None:
            product.pr_mimage=old_img
        else:
            product.pr_mimage=new_img

        old_img=product.pr_simage1
        new_img = request.FILES.get('photo1')
        if old_img !=None and new_img==None:
            product.pr_simage1=old_img
        else:
            product.pr_simage1=new_img

        old_img=product.pr_simage2
        new_img = request.FILES.get('photo2')
        if old_img !=None and new_img==None:
            product.pr_simage2=old_img
        else:
            product.pr_simage2=new_img

        old_img=product.pr_simage3
        new_img = request.FILES.get('photo3')
        if old_img !=None and new_img==None:
            product.pr_simage3=old_img
        else:
            product.pr_simage3=new_img

        product.pr_discost = int(product.pr_cost)-(int(product.pr_cost)*float(int(product.pr_discount)/100)) 

        select_item= request.POST.get('select_item')
        category=CategoryModel.objects.get(id=select_item)
        product.category = category


        product.save()
        return redirect("admin_product_details",product.id)
    
    else:
        return redirect("admin_product_details",product.id)

    
@login_required(login_url='userlogin')
def load_category(request):
    return render(request,'category.html')

@login_required(login_url='userlogin')
def categorycreate(request):
    if request.method=='POST':
        cat_name=request.POST['cname']

        if CategoryModel.objects.filter(cat_name=cat_name).exists():
            messages.info(request, 'This Category Already Exists!!!')
            return redirect('load_category')
            
        else:
            data = CategoryModel(
                cat_name = cat_name)
            data.save()
            messages.info(request, 'Category Added Succesfully')
            return redirect('load_category')
    
    else:
        return render(request,'categorycreate.html')

@login_required(login_url='userlogin')
def load_product_details_fh(request,pk):
    product = ProductModel.objects.get(id=pk)
    categorys = CategoryModel.objects.all()
    products = ProductModel.objects.filter(category=product.category)[0:7]
    return render(request,'product_details_fh.html',{"product":product,"products":products,"categorys":categorys})

@login_required(login_url='userlogin')
def load_product_details_fp(request,pk):
    product = ProductModel.objects.get(id=pk)
    categorys = CategoryModel.objects.all()
    products = ProductModel.objects.filter(category=product.category)[0:7]
    return render(request,'product_details_fp.html',{"product":product,"products":products,"categorys":categorys})

@login_required(login_url='userlogin')
def show_category(request):
    categorys = CategoryModel.objects.all()
    return render(request,'show_category.html',{"categorys":categorys})

@login_required(login_url='userlogin')
def load_category_update(request,pk):
    category = CategoryModel.objects.get(id=pk)
    return render(request,'update_category.html',{"category":category})

@login_required(login_url='userlogin')
def updatecategory(request,pk):
    if request.method=='POST':
        category = CategoryModel.objects.get(id=pk)
        category.cat_name = request.POST.get('cname')
        
        category.save()
        return redirect("show_category")
    return render(request,"category.html")

@login_required(login_url='userlogin')
def deletecategory(request,pk):
    category = CategoryModel.objects.get(id=pk)
    category.delete()
    return redirect('show_category')

@login_required(login_url='userlogin')
def deletecart(request,pk):
    cart = CartModel.objects.get(product=pk)
    cart.delete()
    return redirect('load_cart')

@login_required(login_url='userlogin')
def load_cart(request):
    categorys = CategoryModel.objects.all()
    user=CustomerModel.objects.get(user=request.user.id)
    products = CartModel.objects.filter(user=user)
    if CartModel.objects.filter(user=user.id).exists():
        categorys = CategoryModel.objects.all()
        return render(request,"cart.html",{"products":products,"categorys":categorys,"user":user}) 
    else:
        messages.info(request, 'Cart Is Empty')
        return render(request,"cart.html",{"categorys":categorys,"user":user}) 
    
    
@login_required(login_url='userlogin')
def add_to_cart(request,pk):
    categorys = CategoryModel.objects.all()
    product = ProductModel.objects.get(id=pk)
    user=CustomerModel.objects.get(user=request.user.id)
    if CartModel.objects.filter(user=user).exists():
        ids = CartModel.objects.values_list('product', flat=True).filter(user=user)
        if product.id in ids:
            messages.info(request, 'Product already in Cart')
            return render(request,"product_details_fp.html",{"product":product,"categorys":categorys}) 
        else:
            data = CartModel(
                product=product,
                user=user)
            
            data.save()
            return redirect("load_cart")
    
    else:
        data = CartModel(
            product=product,
            user=user)
        
        data.save()
        return redirect("load_cart")
    
    
@login_required(login_url='userlogin')
def load_order(request):
    user=CustomerModel.objects.get(user=request.user.id)
    if CartModel.objects.filter(user=user).exists():
        return render(request,'order.html')
    
    else:
        messages.info(request, 'Cart is Empty')
        return render(request,'cart.html')



@login_required(login_url='userlogin')
def load_shop(request,pk):
    if ProductModel.objects.filter(category=pk).exists():
        user=CustomerModel.objects.get(user=request.user.id)
        products = ProductModel.objects.filter(category=pk)
        category = products[0].category.cat_name
        categorys = CategoryModel.objects.all()
        return render(request,'shop.html',{"products":products,"category":category,"categorys":categorys,"user":user})

    else:
        return redirect('load_construction')

@login_required(login_url='userlogin')
def load_construction(request):
    return render(request,'underconstruction.html')

@login_required(login_url='userlogin')
def load_show_products(request):
    products = ProductModel.objects.all()
    return render(request,'show_product.html',{"products":products})

@login_required(login_url='userlogin')
def admin_product_details(request,pk):
    product = ProductModel.objects.get(id=pk)
    return render(request,'admin_product_details.html',{"product":product})

@login_required(login_url='userlogin')
def load_show_user(request):
    customers = CustomerModel.objects.all()
    return render(request,'show_user.html',{"customers":customers})

@login_required(login_url='userlogin')
def deleteproduct(request,pk):
    products = ProductModel.objects.all()
    if ProductModel.objects.filter(id=pk).exists():
        product = ProductModel.objects.get(id=pk)
        product.delete()
        messages.info(request, 'Product Deleted')
        return render(request,'show_product.html',{'products':products})
    
    else:
        return render(request,'show_product.html',{'products':products})

@login_required(login_url='userlogin')
def deleteuser(request,pk):
    if CustomerModel.objects.filter(id=pk).exists():
        user = CustomerModel.objects.get(id=pk)
        user.delete()
        messages.info(request, 'User Deleted')
        return redirect('load_show_user')
    
    else:
        return redirect('load_show_user')



@login_required(login_url='userlogin')
def load_user_details(request,pk):
    customer = CustomerModel.objects.get(id=pk)
    return render(request,'user_details.html',{"customer":customer})

@login_required(login_url='userlogin')
def load_edit_product(request,pk):
    product = ProductModel.objects.get(id=pk)
    categorys = CategoryModel.objects.all()
    return render(request,"edit_product.html",{"product":product,"categorys":categorys})

@login_required(login_url='userlogin')
def logout(request):
	auth.logout(request)
	return redirect('load_home')