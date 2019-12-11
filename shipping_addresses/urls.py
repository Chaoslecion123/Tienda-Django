from django.urls import path
from .views import (ShippingAddressListView,ShippingAddressAddView,ShippingAddressEditView,
                    ShippingAddressDeleteView,default)


urlpatterns = [
    path('',ShippingAddressListView.as_view(),name='shipping-addresses'),
    path('crear/',ShippingAddressAddView.as_view(),name='add-shipping'),
    path('editar/<int:pk>/',ShippingAddressEditView.as_view(),name='edit-shipping'),
    path('delete/<int:pk>/',ShippingAddressDeleteView.as_view(),name='delete-shipping'),
    path('default/<int:pk>/',default,name='default')
]
