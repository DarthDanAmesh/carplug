from django.contrib import admin

from store.models import Manufacturer, Importer, Car, CarImporter, Review

admin.site.register(Manufacturer)
admin.site.register(Importer)
admin.site.register(Car)
admin.site.register(CarImporter)
admin.site.register(Review)