from django.urls import path
from .views import apply_code

urlpatterns = [
    path('',apply_code,name='apply_code')
]
