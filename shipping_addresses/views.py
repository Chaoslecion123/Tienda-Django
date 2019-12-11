from django.shortcuts import render,redirect,reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import ShippingAddress
from users.models import User
from .forms import ShippingAddressForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.utils import get_or_create_order
from carts.utils import get_or_create_cart



class ShippingAddressListView(LoginRequiredMixin,ListView):
    login_url = 'login'
    template_name = 'shipping_addresses/shipping_addresses.html'
    model = ShippingAddress

    def get_queryset(self):
        return ShippingAddress.objects.filter(user=self.request.user).order_by('-default')


class ShippingAddressAddView(LoginRequiredMixin,CreateView):
    login_url = 'login'
    #redirect_field_name = 'index'
    template_name = 'shipping_addresses/create.html'
    model = ShippingAddress
    form_class = ShippingAddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = get_object_or_404(User,pk=self.request.user.id)
        return context

    def form_valid(self,form):
        context = self.get_context_data()
        form = context['form']

        with transaction.atomic():
            if form.is_valid():
                shipping_address = form.save(commit=False)
                shipping_address.user = self.request.user
                shipping_address.default = not ShippingAddress.objects.filter(user=self.request.user).exists()
                shipping_address.save()

                if self.request.GET.get('next'):
                    if self.request.GET['next'] == reverse('orders:address'):
                        cart = get_or_create_cart(self.request)
                        order = get_or_create_order(cart,self.request)

                        order.update_shipping_address(shipping_address)

                        return HttpResponseRedirect(self.request.GET['next'])

                messages.success(self.request,'Direccion creada exitosamente')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('shipping_addresses:shipping-addresses')

class ShippingAddressEditView(LoginRequiredMixin,UpdateView):
    login_url = 'login'
    #redirect_field_name = 'index'
    template_name = 'shipping_addresses/edit.html'
    model = ShippingAddress
    form_class = ShippingAddressForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            redirect('carts:cart')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('shipping_addresses:shipping-addresses')


class ShippingAddressDeleteView(LoginRequiredMixin,DeleteView):
    login_url = 'login'
    model = ShippingAddress
    template_name = 'shipping_addresses/delete.html'

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('shipping_addresses:shipping-addresses')

        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')


        if self.get_object().has_orders():
            return redirect('shipping_addresses:shipping-addresses')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('shipping_addresses:shipping-addresses')

def default(request,pk):
    shipping_address = get_object_or_404(ShippingAddress,pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    if request.user.has_shipping_address():
        request.user.shipping_address.update_default()

    shipping_address.update_default(True)

    return redirect('shipping_addresses:shipping-addresses')
