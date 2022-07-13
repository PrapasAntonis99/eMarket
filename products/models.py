from django.conf import settings
from django.db import models
from django.shortcuts import reverse


CATEGORY_CHOICES = (
    ('C', 'Casual'),
    ('SW', 'Sportwear'),
    ('OW', 'Outwear'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('D', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, blank=True, null=True, max_length=2)
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product", kwargs={
            "slug": self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("products:add-to-cart", kwargs={
            "slug": self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("products:remove-from-cart", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
