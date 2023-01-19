from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.utils.http import is_safe_url

from .forms import (
    ProfileForm, 
    EditAddressForm,
    CreateAddressForm)
from base.forms import DivErrorList
from userprofile.models import ShippingAddress


@login_required
def profile_page(request):
    user = request.user
    print(f"Current user {user}")
    addresses = ShippingAddress.objects.filter(user=user)
    print(addresses)
    default_address = None
    other_addresses = None
    if addresses.count() >= 1:
        default_address = addresses.get(default=True)
        other_addresses = addresses.filter(default=False)
    

    if request.method == 'POST':
        u_form = ProfileForm(request.POST, error_class=DivErrorList, instance=user)
        print(u_form)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Successfully updated your information')
            return redirect('profile')
    else:
        u_form = ProfileForm(error_class=DivErrorList, instance=user)

    context = {
        'u_form': u_form
    }
    if addresses:
        context["default_add"] = default_address
        context["other_add"] = other_addresses

    return render(request, 'userprofile/profile.html', context)


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Successfully updated your password')
            return redirect('profile')
        else:
            messages.error(request, f'Please correct the error below')
    else:
        form = PasswordChangeForm(user)
    context = {
        'form': form
    }
    return render(request, 'auth/password_change.html', context)


@login_required
def create_address(request):
    user = request.user
    next_ = request.GET.get('from_ship_next')
    next_post = request.POST.get('from_ship_next')
    redirect_path = next_ or next_post or None

    if request.method == 'POST':
        form_class = CreateAddressForm(request.POST or None, error_class=DivErrorList, instance=user)
        if form_class.is_valid():
            print(form_class.__dict__)
            obj = form_class.save(commit=False)
            obj.address_type = request.POST.get("address_type", "SHIPPING")
            obj.save()
            print(f"obj {obj.address_line_1}")
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
def edit_address(request, pk):
    user=request.user
    address = ShippingAddress.objects.get(user=user, pk=pk)
    if request.method == 'POST':
        form_class = EditAddressForm(request.POST, error_class=DivErrorList, instance=address)
        if form_class.is_valid():
            form_class.save()
            messages.success(request, f'Successfully Updated Your Address')
            return redirect('edit_address')
        else:
            messages.error(request, f'UnSuccessfully UnUpdated Your Address')
    else:
        form_class=EditAddressForm(error_class=DivErrorList, instance=address)

    context = {
        'form':form_class
    }
    return render(request, 'userprofile/edit_address.html', context)


@login_required
def make_default_address(request, pk):
    user = request.user
    curr_default_address = ShippingAddress.objects.get(default=True, user=user)
    curr_default_address.default = False
    curr_default_address.save()

    new_default_address = ShippingAddress.objects.get(pk=pk, user=user)
    new_default_address.default = True
    new_default_address.save()
    return redirect('profile')


@login_required
def remove_address(request, pk):
    user = request.user
    address = ShippingAddress.objects.get(pk=pk)
    address.delete()
    return redirect('profile')
