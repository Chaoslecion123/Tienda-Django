from django.urls import path
from .views import create,BillingProfileListView

app_name = 'billing_profiles'

urlpatterns = [
    path('create/',create,name='create'),
    path('list/',BillingProfileListView.as_view(),name='list')
]
