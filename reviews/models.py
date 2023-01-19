from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save

from base.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    """Reviews given by customers"""
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Review Header'), max_length=200, blank=True)
    rating = models.DecimalField(_('Rating'), max_digits=5, decimal_places=2, null=True,blank=True)
    comments = models.TextField(_('Review Comment'), blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self) -> str:
        return f'{self.product}  by {self.user.username}'


def post_save_num_reviews(sender, instance, created, *args, **kwars):
    if created:
        product_qs = Product.objects.get(_id=instance.product._id)
        product_qs.num_reviews += 1
        product_qs.save()

post_save.connect(post_save_num_reviews, sender=Review)
