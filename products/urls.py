from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
     path('', views.HomeView.as_view(), name='home'),
     path('checkout/', views.checkout, name='checkout'),
     path('product_list/', views.ProductsView.as_view(), name='product_list'),
     path('product/<slug>/', views.ItemDetailView.as_view(), name='product'),
]
