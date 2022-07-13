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
    price = models.IntegerField()
    discount = models.IntegerField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, blank=True, null=True, max_length=2)
    slug = models.SlugField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product", kwargs={
            "slug": self.slug
        })


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.title
