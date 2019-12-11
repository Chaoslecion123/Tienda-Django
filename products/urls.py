from django.urls import path
from .views import ProductDetailView,ProductSearchListView


urlpatterns = [
    path('search/',ProductSearchListView.as_view(),name='search'),
    path('products/detail/<slug:slug>/',ProductDetailView.as_view(),name='product-detail'),
]
