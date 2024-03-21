from django.db import models
import uuid
from accounts.models import Person
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()

UNIT_TYPE = (
    (("Cartoon"), _("Cartoon")),
    (("Bag"), _("Bag")),
    (("Box"), _("Box")),
    (("Pieces"), _("Pieces")),
)

RETURNED_STATUS = (
    ("Invalid",_("Invalid")),
    ("Valid",_("Valid"))
)

STATUS = (
    ("Buyed",_("Buyed")),
    ("Sold Out",_("Sold Out")),
    ("Returned",_("Returned")),
    ("Out of Stock",_("Out of Stock")),
    ("New Raw",_("New Raw")),
    ("In Dyeing",_("In Dyeing")),
    ("In Production",_("In Production")),
)

class Yarn(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    name = models.CharField(_("yarn name"), max_length=50)
    yarn_type = models.CharField(_("yarn type"), max_length=50)

    class Meta:
        verbose_name = _("Yarn")
        verbose_name_plural = _("Yarns")

    def __str__(self):
        return f"{self.name} {self.yarn_type}"

    def get_absolute_url(self):
        return reverse("Yarn_detail", kwargs={"pk":self.id})


class Fabric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    name = models.CharField(_("fabric name"), max_length=50)
    fabric_type = models.CharField(_("fabric type"), max_length=50)

    class Meta:
        verbose_name = _("Fabric")
        verbose_name_plural = _("Fabrics")

    def __str__(self):
        return f"{self.name} {self.fabric_type}"

    def get_absolute_url(self):
        return reverse("Fabric_detail", kwargs={"pk":self.id})
        

class weightPrice(models.Model):
    total_weight = models.DecimalField(_("total weight"), max_digits=10, decimal_places=2)
    unit_type = models.CharField(_("unit type"), max_length=50, choices = UNIT_TYPE, null=True, blank=True)
    quantity_per_unit = models.IntegerField(_("quantity per type"), null=True, blank =True)
    unit_price = models.DecimalField(_("unit price"), max_digits=10, decimal_places=2, null=True, blank =True)
    total_price = models.DecimalField(_("total price"), max_digits=10, decimal_places=2)
    notes = models.TextField(_("notes"), null=True, blank=True)

    class Meta:
        abstract =True  

class YarnInventory(weightPrice):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    yarn = models.ForeignKey(Yarn, verbose_name=_("yarn"), on_delete=models.CASCADE)
    owner = models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    supplier = models.ForeignKey(Person, verbose_name=_("supplier"), on_delete = models.CASCADE)
    actual_existing_weight = models.DecimalField(_("actual existing weight"), max_digits=10, decimal_places=2)
    recieved_at = models.DateTimeField(_("received at"))
    located_at = models.CharField(_("located at"), max_length=50, null=True, blank=True)
    status = models.CharField(_("status"), max_length=50, choices = STATUS, null=True, blank=True)
    discount = models.DecimalField(_("discount"), max_digits=10, decimal_places=2 , null=True, blank=True)
    added_tax =models.DecimalField(_("added tax"), max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name = _("Yarn In Inventory")
        verbose_name_plural = _("Yarns In Inventory")

    def __str__(self):
        return f"{self.yarn} -> {self.supplier} -> {self.total_weight} kg, Exist {self.actual_existing_weight} kg"

    def get_absolute_url(self):
        return reverse("YarnInventory_detail", kwargs={"pk":self.id})
    

class SoldYarn(weightPrice):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, verbose_name=_("Seller"), on_delete=models.CASCADE)
    yarn_inventory = models.ForeignKey(YarnInventory, verbose_name=_("Yarn"), on_delete=models.CASCADE)
    customer = models.ForeignKey(Person, verbose_name=_("Customer"), on_delete = models.CASCADE)
    sold_at = models.DateTimeField(_("Sold At"), auto_now=False, auto_now_add=False)
    added_tax =models.DecimalField(_("added tax"), max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(_("discount"), max_digits=10, decimal_places=2 , null=True, blank=True)

    class Meta:
        verbose_name = _("Sold Yarn")
        verbose_name_plural = _("Sold Yarns")
        ordering = ["yarn_inventory", "customer", "sold_at"]
    def __str__(self):
        return f"{self.total_weight} kg {self.yarn_inventory.yarn} buyed to {self.customer}"

    def get_absolute_url(self):
        return reverse("SoldYarn_detail", kwargs={"pk":self.id})

