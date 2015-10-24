from django.contrib import admin

from .models import Request, Location, Offer
# Register your models here.

admin.site.register(Request, admin.ModelAdmin)
admin.site.register(Location, admin.ModelAdmin)
admin.site.register(Offer, admin.ModelAdmin)
