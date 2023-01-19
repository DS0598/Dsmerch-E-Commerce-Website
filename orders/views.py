from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import is_safe_url

from userprofile.forms import CreateAddressForm
from base.forms import DivErrorList

from userprofile.models import ShippingAddress

# Create your views here.
@login_required
def checkout_create_address(request):
    user = request.user
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        form_class = CreateAddressForm(request.POST or None, error_class=DivErrorList, instance=user)
        if form_class.is_valid():
            print(form_class.__dict__)
            obj = form_class.save(commit=False)
            address_type = request.POST.get("address_type", "SHIPPING")
            obj.address_type = address_type
            obj.save()

            request.session[address_type + "_address_id"] = obj.id
            messages.success(request, f"Successfully created new address")
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('profile')
    else:
        form_class = CreateAddressForm(error_class=DivErrorList, instance=user)

    context = {
        'form': form_class
    }
    return render(request, 'userprofile/create_address.html', context)

@login_required
def checkout_reuse_address(request):
    user = request.user
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        print(request.POST)
        address_type = request.POST.get("address_type", "SHIPPING")
        shipping_address = request.POST.get("shipping_address", None)
        if shipping_address:
            qs = ShippingAddress.objects.filter(user=user, id=shipping_address)
            if qs.exists():
                request.session[address_type + "_address_id"] = shipping_address
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)

    context = {
    }
    return render(request, 'userprofile/create_address.html', context)