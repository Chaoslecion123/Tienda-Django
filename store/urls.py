from django.contrib import admin
from django.urls import path,include
from .views import login_view,logout_view,index,register
from products.views import ProductListView
from products.urls import urlpatterns as products_urls
from carts.urls import urlpatterns as carts_urls
from orders.urls import urlpatterns as orders_urls
from shipping_addresses.urls import urlpatterns as shippingaddresses_urls
from promo_codes.urls import urlpatterns as promo_codes_urls
from billing_profiles.urls import urlpatterns as billing_profiles_urls

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',ProductListView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('usuarios/login/', login_view,name='login'),
    path('usuarios/logout/',logout_view,name='logout'),
    path('usuarios/register/',register,name='register'),
    path('products/',include(
        (
            products_urls,
            'products'
        ),
            namespace='products')
        ),
    path('carts/',include(
        (
            carts_urls,
            'carts'
        ),
        namespace='carts')
        ),
    path('orden/',include(
        (
            orders_urls,
            'orders'
        ),
        namespace='orders')
        ),
    path('shipping_addresses/',include(
        (
            shippingaddresses_urls,
            'shipping_addresses'
        ),
        namespace='shipping_addresses')
            ),
    path('apply/code/',include(
        (
            promo_codes_urls,
            'promo_codes'
        ),
        namespace='promo_codes')
        ),
    path('pagos/',include(
        (
            billing_profiles_urls,
            'billing_profiles'
        ),
        namespace='billing_profiles'
    ))

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)