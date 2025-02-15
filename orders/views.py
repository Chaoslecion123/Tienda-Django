import threading
from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models.query import EmptyQuerySet


from .utils import get_or_create_order, breadcrumb,destroy_order
from .mails import Mail
from carts.utils import get_or_create_cart,destroy_cart
from .decorators import validate_cart_and_order

from django.contrib.auth.decorators import login_required


from .models import Order
from charges.models import Charge
from shipping_addresses.models import ShippingAddress


class OrderListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = 'orders/list.html'

    def get_queryset(self):
        return self.request.user.orders_completed()


@login_required(login_url='login')
@validate_cart_and_order
def order(request,cart,order):
    if not cart.has_product():
        return redirect('carts:cart')

    return render(request,'orders/order.html',{
        'cart':cart,
        'order':order,
        'breadcrumb':breadcrumb
    })


@login_required(login_url='login')
@validate_cart_and_order
def address(request,cart,order):

    if not cart.has_product():
        return redirect('carts:cart')

    shipping_address = order.get_or_set_shipping_address()

    can_choice_address = request.user.has_shipping_addresses()

    return render(request,'orders/address.html',{
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'can_choice_address':can_choice_address,
        'breadcrumb':breadcrumb(address=True),

    })

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.addresses

    return render(request,'orders/select_address.html',{
        'shipping_addresses':shipping_addresses,
        'breadcrumb':breadcrumb(address=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def check_address(request,cart,order,pk):
    shipping_address = get_object_or_404(ShippingAddress,pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart ')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def payment(request,cart,order):

    if not cart.has_product() or order.shipping_address is None:
        return redirect('carts:cart')

    billing_profile = order.get_or_set_billing_profile()

    return render(request,'orders/payment.html',{
        'cart':cart,
        'order':order,
        'billing_profile':billing_profile,
        'breadcrumb':breadcrumb(address=True,payment=True)
    })

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request,cart,order):

    if not cart.has_product() or order.shipping_address is None or order.billing_profile is None:
        return redirect('carts:cart')

    shipping_address = order.shipping_address

    if shipping_address is None:
        return redirect('orders:address')


    return render(request,'orders/confirm.html',{
        'cart':cart,
        'order':order,
        'shipping_address':shipping_address,
        'breadcrumb':breadcrumb(address=True,confirmation=True,payment=True),
    })

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request,cart,order):
    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()
    destroy_order(request)
    destroy_cart(request)
    messages.error(request,'El orden ha sido cancelado')

    return redirect('index')

@login_required(login_url='login')
@validate_cart_and_order
def completed(request,cart,order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    charge = Charge.objects.create_charge(order)
    if charge:
        with transaction.atomic():
            order.completed()

            thread = threading.Thread(target=Mail.send_complete_order,args=(order,request.user))
            thread.start()

            destroy_order(request)
            destroy_cart(request)
            messages.success(request,'El orden ha sido completado exitosamente')

    return redirect('index')
