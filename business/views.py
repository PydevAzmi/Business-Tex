from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import *
from .forms import YarnForm, FabricForm
from django.views import View
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):    
    recent_yarn = YarnInventory.objects.filter(owner = request.user)[:10]
    recent_fabric = FabricInventory.objects.filter(owner = request.user)[:10]
    recent_dyed_fabric = FabricDyeingInventory.objects.filter(owner = request.user)[:10]
    sold_fabrics = SoldFabric.objects.filter(owner = request.user)[:10]
    sold_yarns = SoldYarn.objects.filter(owner = request.user)[:10]

    context = {
        "recent_yarn": recent_yarn,
        "recent_fabric": recent_fabric,
        "recent_dyed_fabric": recent_dyed_fabric,
        "sold_fabrics": sold_fabrics,
        "sold_yarns": sold_yarns,
    }

    return render(request, "business/home.html",context)


class YarnList(View):
    def get(self, request):
        form = YarnForm()
        yarn_list = Yarn.objects.filter(owner = request.user).all()
        return render(request,  "business/list_yarn.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        form = YarnForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:yarn_list")

    def update(self, request, pk):
        instance = get_object_or_404(Yarn, pk=pk)
        form = YarnForm(request.POST,instance = instance)
        if form.is_valid():
            form.save()
            return redirect("business:yarn_list")
        return render(request,  "business/list_yarn.html", {"form": form})
        

class FabricList(View):
    def get(self, request):
        form = FabricForm()
        fabric_list = Fabric.objects.filter(owner = request.user).all()
        return render(request,  "business/list_fabric.html", {'fabric_list': fabric_list, "form": form}) 
    

    def post(self, request):
        form = FabricForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:fabric_list")
