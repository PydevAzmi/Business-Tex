from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Yarn)
admin.site.register(models.Fabric)
admin.site.register(models.YarnInventory)
admin.site.register(models.YarnFactory)
admin.site.register(models.ReturnedYarn)
admin.site.register(models.SoldYarn)
admin.site.register(models.FabricInventory)
admin.site.register(models.FabricDyeingFactory)
admin.site.register(models.FabricDyeingInventory)
admin.site.register(models.SoldFabric)
admin.site.register(models.ReturnedFabric)

