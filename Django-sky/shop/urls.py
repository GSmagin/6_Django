from django.urls import path

from .apps import ShopConfig
from .views import ProductListView, contacts, ProductCreateView, ProductDetailView, ProductUpdateView, ProductDeleteView

app_name = ShopConfig.name

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_list'),
    path('contacts/', contacts, name='contacts'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
