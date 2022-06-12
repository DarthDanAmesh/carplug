from django.contrib.admin import AdminSite

from store.models import Manufacturer, Importer, Car, CarImporter, Review


class CarReviewSite(AdminSite):
    title_header = 'Car Admin'
    site_header = 'Car administration'
    index_title = 'Car site admin'


admin_site = CarReviewSite(name='carzone')

admin_site.register(Manufacturer)
admin_site.register(Importer)
admin_site.register(Car)
admin_site.register(CarImporter)
'''admin.site.register(Review) - provides the CRUD functionality using the reviews.models.Publisher attributes 
in the Review model definition) as schema for the page content. Also, this will be used by the admin app 
to edit the data in our reviews model.'''
admin_site.register(Review)
