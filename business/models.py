from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.text import slugify

# Create your models here.
YARN_UNIT_TYPE = (
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
    actual_weight = ''
    unit_type = ''
    quantity_per_unit = ''
    price_per_kg = ''
    total_price = ''
    recieved_at = ''
    located_at = ''
    notes = ''
    slug = ''

    class Meta:
        verbose_name = _("YarnInventory")
        verbose_name_plural = _("YarnsInventory")

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

    class Meta:
        verbose_name = _("YarnFactory")
        verbose_name_plural = _("YarnsFactory")

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
    quantity_recieved = ''
    quantity_remaining = ''
    pieces = ''
    recieved_at = ''
    notes = ''
    slug = ''

    class Meta:
        verbose_name = _("FabricInventory")
        verbose_name_plural = _("FabricsInventory")

    def __str__(self):
        return self.fabric

    def get_absolute_url(self):
        return reverse("FabricInventory_detail", kwargs={"pk": self.pk})


class FabricDyeing(models.Model):
    fabric = ''
    dyeing_factory = ''
    weigth = ''
    came_out = ''

    class Meta:
        verbose_name = _("FabricDyeing")
        verbose_name_plural = _("FabricsDyeing")

    def __str__(self):
        return self.fabric

    def get_absolute_url(self):
        return reverse("FabricDyeing_detail", kwargs={"pk": self.pk})
