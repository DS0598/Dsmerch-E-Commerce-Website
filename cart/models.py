from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from base.models import Product
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        print(qs)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            print("Creating new cart")
            cart_obj = self.new(user=request.user)
            new_obj = True
            request.session["cart_id"] = cart_obj.id

        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None and user.is_authenticated:
            user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self) -> str:
        return f"{self.id}"

def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        products = instance.products.all()
        total = 0
        for item in products:
            total += item.price
        instance.total = total
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)