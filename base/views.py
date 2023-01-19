from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.http import is_safe_url

from .forms import (
    RegisterForm, 
    LoginForm, 
    DivErrorList, 
    CreateProductForm,
    EditProductForm
)

from reviews.forms import CreateReviewForm

from .models import Product
from userprofile.models import ShippingAddress
from reviews.models import Review
from cart.models import Cart


def register(request):

    if request.method == 'POST':
        form_class = RegisterForm(request.POST or None, error_class=DivErrorList)
        if form_class.is_valid():
            username = form_class.cleaned_data.get('username')
            email = form_class.cleaned_data.get('email')
            password = form_class.cleaned_data.get('password')
            user = User.objects.create_user(username, email, password)
            if user:
                return redirect('login')
        else:
            print("ERROR")
    else:
        form_class = RegisterForm(error_class=DivErrorList)

    context = {
        "form": form_class
    }

    return render(request, 'auth/register.html', context)


def login_page(request):
    next_ = request.GET.get("next")
    next_post = request.POST.get("next")
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        form_class = LoginForm(request.POST or None, error_class=DivErrorList)
        if form_class.is_valid():
            username = form_class.cleaned_data.get('username')
            email = form_class.cleaned_data.get('email')
            password = form_class.cleaned_data.get('password')

            user = authenticate(username=username, email=email, password=password)
            if user:
                login(request, user)
                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)
                else:
                    return redirect('/')
            else:
                messages.error(request, f"Wrong username or password. Please check again.")
                
        else:
            print("ERROR")
    else:
        form_class = LoginForm(error_class=DivErrorList)
    context = {
        "form": form_class
    }
    return render(request, 'auth/login.html', context)


def logout_page(request):
    user = request.user
    if user:
        logout(request)
        return redirect('/')


def products_list(request):
    print(request.session.get("first_name", "Unknown"))
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'pages/products_list.html', context)


def product_detail(request, pk):
    product = Product.objects.get(_id=pk)
    countInStock = range(1, product.count_in_stock + 1)
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    review_form = CreateReviewForm(error_class=DivErrorList)
    review_qs = None
    review_qs = Review.objects.filter(product=product)
    context = {
        "object": product,
        "countInStock": countInStock,
        "reviews": review_qs,
        "review_form": review_form
    }
    context["cart"] = cart_obj
    return render(request, 'pages/product_detail.html', context)


# STAFF VIEWS
def staff_products_list(request):
    if request.user.is_staff == True:
        queryset = Product.objects.all()
        context = {
            'object_list': queryset
    }
    else:
        return redirect('home')
    return render(request, 'staff/staff_products_list.html', context)


def create_product(request):
    if request.user.is_staff == True:
        user = request.user
        if request.method == 'POST':
            form_class = CreateProductForm(request.POST or request.FILES, error_class=DivErrorList, instance=user)
            if form_class.is_valid():
                product = Product.objects.create(user=user)
                product.name = form_class.cleaned_data.get("name")
                if 'image' in request.FILES:
                    product.image = request.FILES['image']
                product.brand = form_class.cleaned_data.get("brand")
                product.category = form_class.cleaned_data.get("category")
                product.description = form_class.cleaned_data.get("description")
                product.price = form_class.cleaned_data.get("price")
                product.count_in_stock = form_class.cleaned_data.get("count_in_stock")
                product.save()
                messages.success(request, f'Created new product')
                return redirect('staff_products_view')
            else:
                messages.error(request, f'Fix error below')
        else:
            form_class = CreateProductForm(error_class=DivErrorList, instance=user)
        context = {
            'form': form_class
    }
    else:
        return redirect('home')

    return render(request, 'staff/create_product.html', context)

def edit_product(request, pk):
    if request.user.is_staff == True:
        user = request.user
        product = Product.objects.get(pk=pk)
        if request.method == 'POST':
            form_class = EditProductForm(request.POST or request.FILES, error_class=DivErrorList, instance=product)
            if form_class.is_valid():
                obj = form_class.save()
                if 'image' in request.FILES:
                    obj.image = request.FILES['image']
                    obj.save()
                messages.success(request, f'Updated product')
                return redirect('staff_products_view')
            else:
                messages.error(request, f'Fix error below')
        else:
            form_class = EditProductForm(error_class=DivErrorList, instance=product)
        context = {
            'form': form_class,
            'obj': product
    }
    else:
        return redirect('home')

    return render(request, 'staff/edit_product.html', context)


def remove_product(request, pk):
    user = request.user
    if user.is_staff == True:
        product = Product.objects.get(pk=pk)
        product_name = product.name
        product.delete()
        messages.success(request, f'Deleted product {product_name}')
        return redirect('staff_products_view')
    else:
        return redirect('home')


def staff_users_list(request):
    if request.user.is_staff == True:
        queryset = User.objects.filter(is_staff=False)
        context = {
            'object_list': queryset
        }
    else:
        return redirect('home')
    return render(request, 'staff/staff_users_list.html', context)


def staff_show_user_detail(request, pk):
    if request.user.is_staff == True:
        user = User.objects.get(pk=pk)
        addresses = ShippingAddress.objects.filter(user=user)
        user_default_address = None
        user_addresses = None
        if addresses.count() >= 1:
            user_default_address = addresses.get(default=True)
            user_addresses = addresses.filter(default=False)
        context = {
            'user_detail': user,
            'addresses': user_addresses,
            'default_address': user_default_address
        }
    else:
        return redirect('home')

    return render(request, 'staff/show_user_details.html', context)



