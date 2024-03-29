from django.db import models
from django.db.models import Sum
import uuid
from accounts.models import Person
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _

User=get_user_model()

UNIT_TYPE=(
    (("Cartoon"), _("Cartoon")),
    (("Bag"), _("Bag")),
    (("Box"), _("Box")),
    (("Pieces"), _("Pieces")),
)

RETURNED_STATUS=(
    ("Invalid",_("Invalid")),
    ("Valid",_("Valid"))
)

STATUS=(
    ("Buyed",_("Buyed")),
    ("Sold Out",_("Sold Out")),
    ("Returned",_("Returned")),
    ("Out of Stock",_("Out of Stock")),
    ("New Raw",_("New Raw")),
    ("In Dyeing",_("In Dyeing")),
    ("In Production",_("In Production")),
)

class Yarn(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    name=models.CharField(_("yarn name"), max_length=50)
    yarn_type=models.CharField(_("yarn type"), max_length=50)

    class Meta:
        verbose_name=_("Yarn")
        verbose_name_plural=_("Yarns")

    def __str__(self):
        return f"{self.name} {self.yarn_type}"

    def get_absolute_url(self):
        return reverse("business:Yarn_detail", kwargs={"pk":self.id})


class Fabric(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    name=models.CharField(_("fabric name"), max_length=50)
    fabric_type=models.CharField(_("fabric type"), max_length=50)

    class Meta:
        verbose_name=_("Fabric")
        verbose_name_plural=_("Fabrics")

    def __str__(self):
        return f"{self.name} {self.fabric_type}"

    def get_absolute_url(self):
        return reverse("business:Fabric_detail", kwargs={"pk":self.id})
        

class Weight(models.Model):
    total_weight=models.DecimalField(_("total weight"), max_digits=10, decimal_places=2)
    unit_type=models.CharField(_("unit type"), max_length=50, choices=UNIT_TYPE, null=True, blank=True)
    quantity_per_unit=models.IntegerField(_("quantity per type"), null=True, blank=True)
    notes=models.TextField(_("notes"), null=True, blank=True)

    class Meta:
        abstract=True  


class Price(models.Model):
    unit_price=models.DecimalField(_("unit price"), max_digits=10, decimal_places=2, null=True, blank=True)
    total_price=models.DecimalField(_("total price"), max_digits=10, decimal_places=2, null=True, blank=True)
    added_tax=models.DecimalField(_("added tax"), max_digits=10, decimal_places=2, null=True, blank=True)
    discount=models.DecimalField(_("discount"), max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        abstract=True  

class YarnInventory(Weight, Price):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    yarn=models.ForeignKey(Yarn, verbose_name=_("yarn"), on_delete=models.CASCADE)
    owner=models.ForeignKey(User, verbose_name=_("owner"), on_delete=models.CASCADE)
    supplier=models.ForeignKey(Person, verbose_name=_("supplier"), on_delete=models.CASCADE)
    recieved_at=models.DateTimeField(_("received at"))
    located_at=models.CharField(_("located at"), max_length=50, null=True, blank=True)
    status=models.CharField(_("status"), max_length=50, choices=STATUS, null=True, blank=True)
    
    class Meta:
        verbose_name=_("Yarn In Stock")
        verbose_name_plural=_("Yarns In Stock")
        ordering = ["-recieved_at"]

    def get_absolute_url(self):
        return reverse("business:YarnInventory_detail", kwargs={"pk":self.id})
    
    def get_existing_weight(self):
        total_out=self.yarnfactory_set.aggregate(total_manufactured=Sum('total_weight'))['total_manufactured'] or 0 # type:ignore
        total_out += self.soldyarn_set.aggregate(total_sold=Sum('total_weight'))['total_sold'] or 0 # type:ignore
        return self.total_weight - total_out
    
    def __str__(self):
        return f"{self.yarn} ({self.total_weight} kg)"

class SoldYarn(Weight, Price):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("Seller"), on_delete=models.CASCADE)
    yarn_inventory=models.ForeignKey(YarnInventory, verbose_name=_("Yarn"), on_delete=models.CASCADE)
    customer=models.ForeignKey(Person, verbose_name=_("Customer"), on_delete=models.CASCADE)
    sold_at=models.DateTimeField(_("Sold At"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name=_("Sold Yarn")
        verbose_name_plural=_("Sold Yarns")
        ordering=["yarn_inventory", "customer", "sold_at"]

    def __str__(self):
        return f"{self.total_weight} kg {self.yarn_inventory.yarn} buyed to {self.customer}"

    def get_absolute_url(self):
        return reverse("business:SoldYarn_detail", kwargs={"pk":self.id})


class YarnFactory(Weight):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    yarn_inventory=models.ForeignKey(YarnInventory, verbose_name=_("Yarn Inventory"), on_delete=models.CASCADE)
    factory=models.ForeignKey(Person, verbose_name=_("Factory"), on_delete=models.CASCADE)
    orderd_at=models.DateTimeField(_("Orderd At"))
    addons_yarn=models.ForeignKey(Yarn, verbose_name=_("addons yarn"), max_length=50, on_delete=models.SET_NULL, null=True, blank=True)
    addons_weigth=models.DecimalField(_("Addons weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    manufactured_fabric=models.ForeignKey("Fabric", verbose_name=_("Manufactured Fabric"), on_delete=models.CASCADE)
    fabric_weight=models.DecimalField(_("Fabric weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    waste_ratio=models.DecimalField(_("Waste Ratio"), max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name=_("Yarn In Factory")
        verbose_name_plural=_("Yarns In Factories")

    def __str__(self):
        return f"{self.total_weight} kg > {self.yarn_inventory.yarn} to {self.factory}"

    def get_absolute_url(self):
        return reverse("business:YarnFactory_detail", kwargs={"pk":self.id})
    
    def save(self, *args, **kwargs ):
        yarn_inv=self.yarn_inventory
        fabric_inventory=FabricInventory.objects.filter(
            owner=yarn_inv.owner,
            yarn_factory=self,
            supplier=self.factory,
            )
        if not fabric_inventory.exists():
            fabric_inventory=FabricInventory.objects.create(
                owner=yarn_inv.owner,
                fabric=self.manufactured_fabric,
                quantity_recieved=0,
                supplier=self.factory,
                located_at=self.factory.name,    
                status="In Production",
                total_weight=0,
                unit_type="Pieces",
                )
            super(YarnFactory, self).save(*args, **kwargs)
            fabric_inventory.yarn_factory=self
            if self.fabric_weight:
                fabric_inventory.total_weight=self.fabric_weight
            fabric_inventory.save()

class ReturnedYarn(Weight):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    yarn_factory=models.ForeignKey(YarnFactory, verbose_name=_("Yarn in Factory"), on_delete=models.CASCADE)
    returned_at=models.DateTimeField(_("Returned At"))
    status=models.CharField(_("Status"), max_length=50, choices=RETURNED_STATUS, null=True, blank=True)

    class Meta:
        verbose_name=_("Returned Yarn")
        verbose_name_plural=_("Returned Yarns")

    def __str__(self):
        return f"{self.total_weight}kg {self.yarn_factory.yarn_inventory.yarn} from {self.yarn_factory.factory.name}"

    def get_absolute_url(self):
        return reverse("business:ReturnedYarn_detail", kwargs={"pk":self.id})


class FabricInventory(Weight, Price):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE)
    fabric=models.ForeignKey(Fabric, verbose_name=_("Faric"), on_delete=models.SET_NULL, null=True, blank=True)
    supplier=models.ForeignKey(Person, verbose_name=_("Factory or Supplier"), on_delete=models.CASCADE)
    yarn_factory=models.ForeignKey(YarnFactory, verbose_name=_("Yarn Factory"), on_delete=models.SET_NULL, null=True, blank=True)
    quantity_recieved=models.DecimalField(_("received weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_remaining=models.DecimalField(_("remaining weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_out_dyeing=models.DecimalField(_("out dyeing weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_buyied=models.DecimalField(_("buyied"), max_digits=10, decimal_places=2, null=True, blank=True)
    recieved_at=models.DateTimeField(_("received At"), null=True, blank=True)
    located_at=models.CharField(_("Located at"), max_length=50, null=True, blank=True)
    status=models.CharField(_("Status"), max_length=50, choices=STATUS, null=True, blank=True)
    

    class Meta:
        verbose_name=_("Fabric In Stock")
        verbose_name_plural=_("Fabrics In Stock")

    def get_existing_weight(self):
        total_out=self.fabricdyeingfactory_set.aggregate(total_produced=Sum('total_weight'))['total_produced'] or 0 # type:ignore
        total_out += self.soldfabric_set.aggregate(total_sold=Sum('total_weight'))['total_sold'] or 0 # type:ignore
        total_out += self.returnedfabric_set.aggregate(total_returned=Sum('total_weight'))['total_returned'] or 0 # type:ignore
        return self.total_weight - total_out

    def __str__(self):
        return f"{self.get_existing_weight() } kg {self.fabric} - {self.supplier}"

    def get_absolute_url(self):
        return reverse("business:FabricInventory_detail", kwargs={"pk":self.id})
    

class ReturnedFabric(Weight):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fabric_inventory=models.ForeignKey(FabricInventory, verbose_name=_("Fabric Inventory"), on_delete=models.CASCADE)
    returned_at=models.DateTimeField(_("Returned At"))
    status=models.CharField(_("Status"), max_length=50, choices=RETURNED_STATUS, null=True, blank=True)

    class Meta:
        verbose_name=_("Returned Fabric")
        verbose_name_plural=_("Returned Fabrics")

    def __str__(self):
        return f"{self.total_weight} to {self.fabric_inventory.supplier.name}"

    def get_absolute_url(self):
        return reverse("business:ReturnedFabric_detail", kwargs={"pk":self.id})


class FabricDyeingFactory(Weight):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fabric_inv=models.ForeignKey(FabricInventory, verbose_name=_("Fabric Inventory"), on_delete=models.CASCADE)
    dyeing_factory=models.ForeignKey(Person, verbose_name=_("Dyeing Factory"), on_delete=models.CASCADE)
    came_out_at=models.DateTimeField(_("Came Out At"))

    class Meta:
        verbose_name=_("Fabric went for Dyeing Factory")
        verbose_name_plural=_("Fabrics went for Dyeing Factories")

    def __str__(self):
        return f"{self.fabric_inv.fabric} to {self.dyeing_factory}"
    
    def save(self, *args, **kwargs ):
        d_fabric_inventory=FabricDyeingInventory.objects.filter(
                fabric_dyeing_factory=self,
                owner=self.fabric_inv.owner,
                supplier=self.dyeing_factory,
            )
        if not d_fabric_inventory.exists():
            d_fabric_inventory=FabricDyeingInventory.objects.create(
                owner=self.fabric_inv.owner,
                fabric=self.fabric_inv.fabric,
                supplier=self.dyeing_factory,
                located_at=self.dyeing_factory.name, 
                status="In Dyeing",
                total_weight=0,
                )
            super(FabricDyeingFactory, self).save(*args, **kwargs)
            d_fabric_inventory.fabric_dyeing_factory=self
            d_fabric_inventory.save()
        super(FabricDyeingFactory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("business:FabricDyeingFactory_detail", kwargs={"pk":self.id})
    

class FabricDyeingInventory(Weight, Price):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.CASCADE)
    fabric=models.ForeignKey(Fabric, verbose_name=_("Fabric"), on_delete=models.CASCADE)
    supplier=models.ForeignKey(Person, verbose_name=_("Supplier"), on_delete=models.CASCADE)
    fabric_dyeing_factory=models.ForeignKey(FabricDyeingFactory, verbose_name=_("Fabric Dyeing Factory"), on_delete=models.CASCADE, null=True, blank=True)
    quantity_recieved=models.DecimalField(_("received weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_remaining=models.DecimalField(_("Remaining weight"), max_digits=10, decimal_places=2, null=True, blank=True)
    quantity_buyied=models.DecimalField(_("buyied"), max_digits=10, decimal_places=2, null=True, blank=True)
    recieved_at=models.DateTimeField(_("received At"), auto_now=False, auto_now_add=False, null=True, blank=True)
    status=models.CharField(_("Status"), max_length=50, choices=STATUS, null=True, blank=True)
    located_at=models.CharField(_("located at"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name=_("Dyed fabric in stock")
        verbose_name_plural=_("Dyed fabrics in stock")
    
    def get_existing_weight(self):
        total_out = self.soldfabric_set.aggregate(total_sold=Sum('total_weight'))['total_sold'] or 0 # type:ignore
        return self.total_weight - total_out
    
    def __str__(self):
        return f"{self.get_existing_weight()}kg {self.fabric} from {self.supplier}"

    def get_absolute_url(self):
        return reverse("business:FabricDyeingInventory_detail", kwargs={"pk":self.id})


class SoldFabric(Weight, Price):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner=models.ForeignKey(User, verbose_name=_("Seller"), on_delete=models.CASCADE)
    fabric_dyeing_inventory=models.ForeignKey(FabricDyeingInventory, verbose_name=_("Fabric Dyeing Inventory"), on_delete=models.CASCADE, null=True, blank=True)
    Fabric_Inventory=models.ForeignKey(FabricInventory, verbose_name=_("Fabric Inventory"), on_delete=models.CASCADE, null=True, blank=True)
    customer=models.ForeignKey(Person, verbose_name=_("Customer"), on_delete=models.CASCADE)
    sold_at=models.DateTimeField(_("Sold At"))

    class Meta:
        verbose_name=_("Sold Fabric")
        verbose_name_plural=_("Sold Fabrics")

    def __str__(self):
        return f"{self.customer} {self.total_weight}"

    def get_absolute_url(self):
        return reverse("business:SoldFabric_detail", kwargs={"pk":self.id})
