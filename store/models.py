from django.db import models
from django.contrib import auth


# Create your models here.

class Manufacturer(models.Model):
    """A company that makes cars."""
    name = models.CharField(max_length=50, help_text="The name of the Manufacturer.")
    website = models.URLField(help_text="The Manufacturer's website.")
    email = models.EmailField(help_text="The Manufacturer's email address.")

    def __str__(self):
        return self.name


class Importer(models.Model):
    """
    A importer to a Car, e.g. International, Local, \
    Inter-Local.
    """
    first_names = models.CharField(max_length=50, help_text="The importer's first name or names.")
    last_names = models.CharField(max_length=50, help_text="The importer's last name or names.")
    email = models.EmailField(help_text="The contact email for the importer.")

    def __str__(self):
        return self.first_names


class Car(models.Model):
    name = models.CharField(max_length=70, help_text="The title of the car.")
    manufacture_date = models.DateField(verbose_name="Date the car was manufactured.")
    fuel_type = models.CharField(max_length=20, verbose_name="Fuel option.")
    mileage = models.CharField(max_length=20, verbose_name="total mileage")
    price = models.IntegerField(verbose_name="current price")
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='store/%Y/%m/%d', blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    importers = models.ManyToManyField(Importer, through="CarImporter")

    class Meta:
        ordering = ('available',)

    def __str__(self):
        return "{} ({})".format(self.name, self.manufacture_date)


class CarImporter(models.Model):
    class ImportationRole(models.TextChoices):
        INTERNATIONAL = "INTERNATIONAL", "International"
        LOCAL = "LOCAL", "Local"
        INTER_LOCAL = "INTER-LOCAL", "Inter-Local"

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    importer = models.ForeignKey(Importer, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="The role this importer had in the car.", choices=ImportationRole.choices,
                            max_length=20)

    def __str__(self):
        return f' {self.importer} is selling {self.car} location {self.role} '


class Review(models.Model):
    content = models.TextField(help_text="The Review text.")
    rating = models.IntegerField(help_text="The rating the reviewer has given.")
    date_created = models.DateTimeField(auto_now_add=True, help_text="The date and time the review was created.")
    date_edited = models.DateTimeField(null=True, help_text="The date and time the review was last edited.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, help_text="The Car that this review is for.")

    def __str__(self):
        return f'{self.car}'
