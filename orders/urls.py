from django.urls import path
from .views import order,address,select_address,check_address,confirm,cancel,completed,OrderListView,payment

app_name = 'orders'

urlpatterns = [
    path('',order,name='order'),
    path('direccion/',address,name='address'),
    path('escoger/',select_address,name='select-address'),
    path('establecer/<int:pk>/',check_address,name='check-address'),
    path('confirmar/',confirm,name='order-confirm'),
    path('cancelar/',cancel,name='cancel'),
    path('completado/',completed,name='completed'),
    path('listado/',OrderListView.as_view(),name='order-list'),
    path('pago/',payment,name='payment')
]
