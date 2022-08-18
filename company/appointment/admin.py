from django.contrib import admin
from .models import Client, PriceList, Appointment, Basket, Masters

admin.site.register(Client)
admin.site.register(PriceList)
admin.site.register(Appointment)
admin.site.register(Basket)
admin.site.register(Masters)
