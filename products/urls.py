from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
     path('', views.HomeView, name='home'),
     path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
     path('product-list/', views.ProductsView.as_view(), name='product-list'),
     path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
     path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
     path('remove-from-cart/<slug>/', views.remove_from_cart, name='remove-from-cart'),
     path('remove-item-from-cart/<slug>/', views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
     path('show-categories/', views.ShowCategories, name='show-categories'),

     path('create-user/', views.create_user, name='create-user'),
]
