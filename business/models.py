from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.text import slugify

# Create your models here.
UNIT_TYPE = (
    (_("Cartoon"), _("Cartoon")),
    (_("Bag"), _("Bag")),
    (_("Box"), _("Box")),
    (_("Pieces"), _("Pieces")),
)

class Yarn(models.Model):
    name = ''
    type = ''

    class Meta:
        verbose_name = _("Yarn")
        verbose_name_plural = _("Yarns")

    def __str__(self):
        return f"{self.name} {self.type}"

    def get_absolute_url(self):
        return reverse("Yarn_detail", kwargs={"pk": self.pk})
    

class YarnInventory(models.Model):
    yarn = ''
    owner = ''
    supplier = ''
    total_weight_in_kg = ''
    actual_existing_weight = ''
    unit_type = ''
    quantity_per_unit = ''
    price_per_kg = ''
    total_price = ''
    recieved_at = ''
    located_at = ''
    notes = ''
    slug = ''

    class Meta:
        verbose_name = _("Yarn In Inventory")
        verbose_name_plural = _("Yarns In Inventory")

    def __str__(self):
        return f"{self.yarn} {self.supplier}"

    def get_absolute_url(self):
        return reverse("YarnInventory_detail", kwargs={"pk": self.pk})


class YarnFactory(models.Model):
    yarn = ''
    factory = ''
    weight_in_kg = ''
    unit_type = ''
    quantity_per_unit = ''
    notes = ''
    orderd_at = ''
    manufactured_fabric = ''
    fabric_weight = ''
    status = ''

    class Meta:
        verbose_name = _("Yarn In Factory")
        verbose_name_plural = _("Yarns In Factories")

    def __str__(self):
        return self.yarn

    def get_absolute_url(self):
        return reverse("YarnFactory_detail", kwargs={"pk": self.pk})


class Fabric(models.Model):
    name = ''
    type = ''

    class Meta:
        verbose_name = _("Fabric")
        verbose_name_plural = _("Fabrics")

    def __str__(self):
        return f"{self.name} {self.type}"

    def get_absolute_url(self):
        return reverse("Fabric_detail", kwargs={"pk": self.pk})
    

class FabricInventory(models.Model):
    owner = ''
    fabric = ''
    factory = ''
    total_weight =''
    manufactured_quantity_recieved = ''
    manufactured_quantity_remaining = ''
    pieces = ''
    recieved_at = ''
    notes = ''
    status = ''
    slug = ''

    class Meta:
        verbose_name = _("Fabric In Inventory")
        verbose_name_plural = _("Fabrics In Inventory")

    def __str__(self):
        return self.fabric

    def get_absolute_url(self):
        return reverse("FabricInventory_detail", kwargs={"pk": self.pk})

class FabricDyeingInventory(models.Model):
    owner = ''
    fabric = ''
    dyeing_factory = ''
    total_weight =''
    dyed_quantity_recieved = ''
    dyed_quantity_remaining = ''
    pieces = ''
    recieved_at = ''
    notes = ''
    status = ''
    slug = ''

    class Meta:
        verbose_name = _("Dyed fabric in stock")
        verbose_name_plural = _("Dyed fabrics in stock")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("FabricDyeingInventory_detail", kwargs={"pk": self.pk})


class FabricDyeingFactory(models.Model):
    fabric = ''
    dyeing_factory = ''
    weigth = ''
    unit_type = ''
    quantity_per_unit = ''
    came_out_at = ''

    class Meta:
        verbose_name = _("Fabric that went for Dyeing Factory")
        verbose_name_plural = _("Fabrics that went for Dyeing Factories")

    def __str__(self):
        return self.fabric

    def get_absolute_url(self):
        return reverse("FabricDyeingFactory_detail", kwargs={"pk": self.pk})


class SoldFabric(models.Model):
    fabric = ''
    customer = ''
    weigth = ''
    unit_type = ''
    quantity_per_unit = ''
    price_per_kg = ''
    total_price = ''
    sold_at = ''
    notes = ''
    slug = ''
    

    class Meta:
        verbose_name = _("Sold Fabric")
        verbose_name_plural = _("Sold Fabrics")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("SoldFabric_detail", kwargs={"pk": self.pk})
