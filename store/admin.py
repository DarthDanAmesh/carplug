from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.utils import OperationalError
from store.models import Manufacturer, Importer, Car, CarImporter, Review, Cart, Order, OrderItem, Wishlist

class CarReviewSite(AdminSite):
    title_header = 'CarZone Admin'
    site_header = 'CarZone Administration'
    index_title = 'CarZone Site Admin'

# Create custom admin site instance
admin_site = CarReviewSite(name='carzone')

# Custom ModelAdmin classes for better admin interface
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded_year')
    search_fields = ('name', 'country')
    list_filter = ('country',)

class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'price', 'available', 'manufacture_date')
    list_filter = ('manufacturer', 'available', 'fuel_type')
    search_fields = ('name', 'manufacturer__name')
    raw_id_fields = ('manufacturer',)
    date_hierarchy = 'manufacture_date'
    ordering = ('-available', 'name')

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'quantity', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'car__name')
    date_hierarchy = 'date_added'

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'creator', 'rating', 'date_created')
    list_filter = ('rating', 'date_created')
    search_fields = ('car__name', 'creator__username', 'content')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order_date', 'total_amount', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'id')
    date_hierarchy = 'order_date'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'car', 'quantity', 'price')
    search_fields = ('order__id', 'car__name')

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('user__username', 'car__name')

# Safe model registration with error handling
def safe_register(model, model_admin=None):
    try:
        if model_admin:
            admin_site.register(model, model_admin)
        else:
            admin_site.register(model)
    except OperationalError:
        # Skip registration if table doesn't exist yet
        pass

# Register models with admin site
safe_register(Manufacturer, ManufacturerAdmin)
safe_register(Importer)
safe_register(Car, CarAdmin)
safe_register(Cart, CartAdmin)
safe_register(Order, OrderAdmin)
safe_register(OrderItem, OrderItemAdmin)
safe_register(Wishlist, WishlistAdmin)
safe_register(CarImporter)
safe_register(Review, ReviewAdmin)