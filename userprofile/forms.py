from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField
from userprofile.models import ShippingAddress


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(
            attrs={
                "class": "form-control my-2",
                "placeholder": "Your email"
            }
        )
    )
    first_name = forms.CharField(label='First Name (Optional)', 
        required=False,
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"First Name"
            }
        )
    )
    last_name = forms.CharField(label='Last Name (Optional)', 
        required=False,
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Last Name"
            }
        )
    )

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
        ]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get("email")
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")
        user.save()
        return user


class CreateAddressForm(forms.ModelForm):
    name = forms.CharField(label='Address Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    contact_number = forms.CharField(label='Contact Number',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    # address_type = forms.ChoiceField(label='Address Type:', required=True,
    #     choices=ShippingAddress.TYPE_OF_ADDRESS,
    #     widget=forms.RadioSelect
    # )

    address_line_1 = forms.CharField(label='Address Line 1',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    address_line_2 = forms.CharField(label='Address Line 2', required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    city = forms.CharField(label='City Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    state = forms.CharField(label='State Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2"
            }
        )
    )
    pincode = forms.CharField(label='Pincode',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2"
            }
        )
    )
    country = CountryField(blank_label='(Select Country)').formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "form-select my-2" 
            }
        )
    )

    class Meta:
        model = ShippingAddress
        fields = [
            'name',
            'contact_number',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'pincode',
            'country',
        ]

    @transaction.atomic
    def save(self, commit=False):
        user = super().save(commit=False)
        address = ShippingAddress.objects.create(user=user)
        address.name = self.cleaned_data.get("name")
        address.contact_number = self.cleaned_data.get("contact_number")
        # address.address_type = self.cleaned_data.get("address_type")
        address.address_line_1 = self.cleaned_data.get('address_line_1')
        address.address_line_2 = self.cleaned_data.get('address_line_2')
        address.city = self.cleaned_data.get('city')
        address.state = self.cleaned_data.get('state')
        address.pincode = self.cleaned_data.get('pincode')
        address.country = self.cleaned_data.get('country')
        address.save()
        return address


class EditAddressForm(forms.ModelForm):
    name = forms.CharField(label='Address Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    contact_number = forms.CharField(label='Contact Number',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    address_line_1 = forms.CharField(label='Address Line 1',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    address_line_2 = forms.CharField(label='Address Line 2',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    city = forms.CharField(label='City Name',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )
    state = forms.CharField(label='State Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2"
            }
        )
    )
    pincode = forms.CharField(label='Pincode',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2"
            }
        )
    )
    country = CountryField(blank_label='(Select Country)').formfield(
        widget=CountrySelectWidget(
            attrs={
                "class": "form-select my-2" 
            }
        )
    )
    
    class Meta:
        model = ShippingAddress
        fields = [
            'name',
            'contact_number',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'pincode',
            'country',
        ]