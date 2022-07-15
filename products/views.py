from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order, Category
from django.utils.translation import gettext as _

from django.contrib.auth.models import User


class ProductsView(ListView):
    model = Item
    paginate_by = 3
    template_name = "product-list.html"

    def get_context_data(self,**kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class HomeView(ListView):
    model = Item
    paginate_by = 3
    template_name = "home.html"


class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order-summary.html', context)
        except ObjectDoesNotExist:
            return redirect("/")


def ShowCategories(request):
    item = Item.objects.all()
    category = request.GET.get('category')
    item = Item.objects.filter(category__name=category)
    categories = Category.objects.all()
    context = {
        'items': item,
        'categories': categories,
    }
    return render(request, 'product-list.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, _("This item quantity was updated."))
            return redirect("products:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, _("This item was added to your cart."))
            return redirect("products:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, _("This item was added to your cart."))
        return redirect("products:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, _("This item was removed from your cart."))
            return redirect("products:order-summary")
        else:
            return redirect("products:product", slug=slug)
    else:
        return redirect("products:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, _("This item quantity was updated."))
            return redirect("products:order-summary")
        else:
            return redirect("products:product", slug=slug)
    else:
        return redirect("products:product", slug=slug)

def create_user(self):
    user = User.objects.create_user(username='john', email='jlennon@beatles.com', password='johntest')
    user.save()
    return redirect("products:home")