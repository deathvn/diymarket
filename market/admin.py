from django.contrib import admin

# Register your models here.
from .models import Order, OrderMatching

admin.site.register(Order)
admin.site.register(OrderMatching)
