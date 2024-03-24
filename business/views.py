from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
    """
    Recently Added Yarns
    Recently Added Fabrics
    Recently Added Dyied Fabrics
    Last Sold Fabrics
    Last Sold yarns
    """
    
    recent_yarn = YarnInventory.objects.all()[:10]
    recent_fabric = FabricInventory.objects.all()[:10]
    recent_dyed_fabric = FabricDyeingInventory.objects.all()[:10]
    sold_fabrics = SoldFabric.objects.all()[:10]
    sold_yarns = SoldYarn.objects.all()[:10]

    context = {
        "recent_yarn": recent_yarn,
        "recent_fabric": recent_fabric,
        "recent_dyed_fabric": recent_dyed_fabric,
        "sold_fabrics": sold_fabrics,
        "sold_yarns": sold_yarns,
    }

    return render(request, "business/home.html",context)



