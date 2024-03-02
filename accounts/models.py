from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _

def profile_image_path(instance, file_name):
    return f"user/{instance.username}/profile_photos/{file_name}"

SYSTEM_ROLES = (
    (("Factory"), _("Factory")),
    (("Supplier"), _("Supplier")),
    (("Customer"), _("Customer")),
    (("Dyeing Factory"), _("Dyeing Factory")),
)

class Location(models.Model):
    country = CountryField(_("Country"), default = "Egypt")
    city = models.CharField(_("City"), max_length=50)
    address = models.CharField(_("address 1"), max_length=50)
    address_2 = models.CharField(_("address 2"), max_length=50, null=True,blank=True)

class User(AbstractUser, Location):
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=11 )
    wa_phone = models.CharField(_("Whatsapp Phone Number"), max_length=11, unique=True) 
    profile_image = models.ImageField(_("Profile Image"),upload_to=profile_image_path, null=True,blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", 'phone_number']


class Person(Location):
    name = models.CharField(_("Name"),max_length=150)
    email =models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=150)
    wa_phone = models.CharField(_("Whatsapp Phone Number"), max_length=11, unique=True) 
    role = models.CharField(_("Role"), max_length=50, choices=SYSTEM_ROLES )
