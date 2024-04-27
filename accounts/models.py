import uuid
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext as _

def profile_image_path(instance, file_name):
    return f"user/{instance.username}/profile_photos/{file_name}"

def company_logo_path(instance, file_name):
    return f"user/{instance.owner}/company_logo/{file_name}"

SYSTEM_ROLES = (
    (("Factory"), _("Factory")),
    (("Supplier"), _("Supplier")),
    (("Customer"), _("Customer")),
    (("Dyeing Factory"), _("Dyeing Factory")),
)

class Location(models.Model):
    country = CountryField(_("Country"), default = "Egypt", null=True,blank=True)
    city = models.CharField(_("City"), max_length=50, null=True,blank=True)
    address = models.CharField(_("address 1"), max_length=50, null=True,blank=True)
    address_2 = models.CharField(_("address 2"), max_length=50, null=True,blank=True)
    
    class Meta:
        abstract = True

class User(AbstractUser, Location):
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    phone_number = models.CharField(_("Phone Number"), max_length=13 )
    wa_phone = models.CharField(_("Whatsapp Phone Number"), max_length=13) 
    profile_image = models.ImageField(_("Profile Image"),upload_to=profile_image_path, null=True,blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", 'phone_number']

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):  
        return self.email 

    def get_absolute_url(self):
        return reverse("User_detail", kwargs={"pk": self.pk})

class Person(Location):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE)
    name = models.CharField(_("Name"),max_length=150)
    email =models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=13)
    wa_phone = models.CharField(_("Whatsapp Phone Number"), max_length=13) 
    role = models.CharField(_("Role"), max_length=50, choices=SYSTEM_ROLES )

    class Meta:
        verbose_name = _("Person")
        verbose_name_plural = _("Persons")
        ordering = ['role']
        
    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("business:Person_detail", kwargs={"pk": self.pk})


class Company(Location):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE )
    name = models.CharField(_("Name"),max_length=150)
    email = models.EmailField(_("Email"), max_length=254, null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=13)
    wa_phone = models.CharField(_("Whatsapp Phone Number"), max_length=13) 
    logo = models.ImageField(_("Logo"), upload_to=company_logo_path  )
    bio = models.CharField(_("Bio"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")

    def __str__(self):
        return f"{self.name} {self.owner}"

    def get_absolute_url(self):
        return reverse("Company_detail", kwargs={"pk": self.pk})