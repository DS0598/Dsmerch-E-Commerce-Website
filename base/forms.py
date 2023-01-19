from urllib import request
from django import forms
from django.forms.utils import ErrorList
from django.db import transaction

from base.models import Product


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="error alert alert-danger mt-1">%s</div>' % e for e in self])


class RegisterForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Your username"
                }
            )
    )
    email = forms.EmailField(
            widget=forms.EmailInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Your email"
                }
            )
    )
    password = forms.CharField(
            widget=forms.PasswordInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Enter password..."
                }
            ))
    password2 = forms.CharField(label="Confirm Password", 
            widget=forms.PasswordInput(
                attrs={
                    "class": "form-control my-2",
                    "placeholder": "Confirm password..."
                }
    ))

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password2 != password:
            raise forms.ValidationError("Password should match.")
        return data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder": "Your Username"
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Your email"
            }
        )
    )
    password = forms.CharField(label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Password"
            }
        )
    )


class CreateProductForm(forms.ModelForm):
    name = forms.CharField(label='Product Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Enter Product Name"
            }
        )
    )

    image = forms.ImageField(label="Product Image",
        required=False, 
        help_text="Upload Image",
        widget=forms.FileInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )

    brand = forms.CharField(label='Brand Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Enter Brand Name"
            }
        )
    )

    category = forms.ChoiceField(label='Product Category',
        choices=Product.TYPE_OF_PRODUCT,
        widget=forms.RadioSelect
    )

    description = forms.CharField(label='Product Description',
        widget=forms.Textarea(
            attrs={
                "class":"form-control my-2"
            }
        )
    )

    price = forms.DecimalField(label='Product Price',
        max_digits=7, decimal_places=2
    )

    count_in_stock = forms.CharField(label='Count in Stock',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'image',
            'brand',
            'category',
            'description',
            'price',
            'count_in_stock',
        ]


class EditProductForm(forms.ModelForm):
    name = forms.CharField(label='Product Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Enter Product Name"
            }
        )
    )

    image = forms.ImageField(label="Product Image",
        required=False, 
        help_text="Upload Image",
        widget=forms.FileInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )

    brand = forms.CharField(label='Brand Name',
        widget=forms.TextInput(
            attrs={
                "class":"form-control my-2",
                "placeholder":"Enter Brand Name"
            }
        )
    )

    category = forms.ChoiceField(label='Product Category',
        choices=Product.TYPE_OF_PRODUCT,
        widget=forms.RadioSelect
    )

    description = forms.CharField(label='Product Description',
        widget=forms.Textarea(
            attrs={
                "class":"form-control my-2"
            }
        )
    )

    price = forms.DecimalField(label='Product Price',
        max_digits=7, decimal_places=2
    )

    count_in_stock = forms.CharField(label='Count in Stock',
        widget=forms.TextInput(
            attrs={
                "class": "form-control my-2"
            }
        )
    )

    class Meta:
        model = Product
        fields = [
            'name',
            'image',
            'brand',
            'category',
            'description',
            'price',
            'count_in_stock',
        ]


