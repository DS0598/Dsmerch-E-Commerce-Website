from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.contrib.auth.models import User


class Product(models.Model):
    """Product table"""
    GAMES = "GAMING"
    MOVIES = "MOVIES"
    SHOWS = "SHOWS"
    COMICS = "COMICS"
    TYPE_OF_PRODUCT = [
        (GAMES, 'Games'),
        (MOVIES, 'Movies'),
        (SHOWS, 'Shows'),
        (COMICS, 'Comics'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Product Name'), max_length=100, blank=True)
    image = models.ImageField(_('Product Image'), null=True, blank=True, upload_to="images", default="images/default_img.png")
    brand = models.CharField(_('Brand Name'), max_length=100, blank=True)
    category = models.CharField(_('Product Type/Category'), max_length=100, choices=TYPE_OF_PRODUCT, blank=True)
    description = models.TextField(_('Product Description'), blank=True)
    rating = models.DecimalField(_('Product Rating'), max_digits=7, decimal_places=1, null=True, blank=True)
    num_reviews = models.IntegerField(_('No. of Reviews'), default=0, null=True, blank=True)
    price = models.DecimalField(_('Price'), max_digits=7, decimal_places=2, null=True, blank=True)
    count_in_stock = models.IntegerField(_('Count in stock'), default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name


