from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import YarnForm, FabricForm, PersonForm
from accounts.models import Person
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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


class YarnList(LoginRequiredMixin, View):
    def get(self, request):
        form = YarnForm()
        yarn_list = Yarn.objects.filter(owner=request.user).all()
        return render(request, "business/products/list_yarn.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        form = YarnForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
            return redirect("business:yarn_list")
        else:
            yarn_list = Yarn.objects.filter(owner=request.user).all()
            return render(request, "business/products/list_yarn.html", {'yarn_list': yarn_list, "form": form})

class YarnDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        yarn = get_object_or_404(Yarn, owner=request.user, id = pk)
        form = YarnForm(instance=yarn)
        return render(request, "business/products/yarn_detail.html", {"form": form})
        
    def post(self, request, pk):
        yarn = get_object_or_404(Yarn, owner=request.user, id = pk)
        form = YarnForm(request.POST, instance=yarn)
        if form.is_valid():
            form.save()
            return redirect("business:yarn_list")
        else:
            yarn = get_object_or_404(Yarn, owner=request.user, id = pk)
            form = YarnForm(request.POST, instance=yarn)
            return render(request, "business/products/yarn_detail.html", {"form": form})

class YarnDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        yarn = get_object_or_404(Yarn, owner=request.user, id = pk)
        yarn.delete()
        return redirect("business:yarn_list")


class FabricList(LoginRequiredMixin, View):
    def get(self, request):
        form = FabricForm()
        fabric_list = Fabric.objects.filter(owner = request.user).all()
        return render(request,  "business/products/list_fabric.html", {'fabric_list': fabric_list, "form": form}) 
    

    def post(self, request):
        form = FabricForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:fabric_list")
        
        
class FabricDetail(LoginRequiredMixin,View):
    def get(self, request, pk):
        fabric = get_object_or_404(Fabric, owner=request.user, id = pk)
        form = FabricForm(instance=fabric)
        return render(request, "business/products/fabric_detail.html", {"form": form})
        
    def post(self, request, pk):
        fabric = get_object_or_404(Fabric, owner=request.user, id = pk)
        form = FabricForm(request.POST, instance=fabric)
        if form.is_valid():
            form.save()
            return redirect("business:fabric_list")
        else:
            fabric = get_object_or_404(Fabric, owner=request.user, id = pk)
            form = FabricForm(request.POST, instance=fabric)
            return render(request, "business/products/fabric_detail.html", {"form": form})

class FabricDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        fabric = get_object_or_404(Fabric, owner=request.user, id = pk)
        fabric.delete()
        return redirect("business:fabric_list")


class PersonList(LoginRequiredMixin, View):
    def get(self, request):
        form = PersonForm()
        path = request.path
        if  path == "/customers/" :
            person_list = Person.objects.filter(owner = request.user, role = "Customer").all()
        elif  path == "/suppliers/" :
            person_list = Person.objects.filter(owner = request.user, role = "Supplier").all()
        elif path == "/factories/":
            person_list = Person.objects.filter(owner = request.user, role = "Factory").all()
        elif path == "/dyeing-factories/":
            person_list = Person.objects.filter(owner = request.user, role = "Dyeing Factory").all()
        return render(request, "business/parteners/person_list.html", {'person_list': person_list, "form": form}) 
    
    def post(self, request):
        form = PersonForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            path = request.path
            if path == "/customers/" :
                myform.role = "Customer"
                myform.save()
                return redirect("business:customers_list")
            elif path == "/suppliers/" :
                myform.role = "Supplier"
                myform.save()
                return redirect("business:suppliers_list")
            elif path == "/factories/":
                myform.role = "Factory"
                myform.save()
                return redirect("business:factories_list")
            elif path == "/dyeing-factories/":
                myform.role = "Dyeing Factory"
                myform.save()
                return redirect("business:dyeing_factories_list")
                            
        
class PersonDetail(LoginRequiredMixin,View):
    def get(self, request, pk):
        person = get_object_or_404(Person, owner=request.user, id = pk)
        form = PersonForm(instance=person)
        return render(request, "business/parteners/person_detail.html", {"form": form})
        
    def post(self, request, pk):
        person = get_object_or_404(Person, owner=request.user, id = pk)
        role =  person.role
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            if role == "Customer" :
                return redirect("business:customers_list")
            elif role == "Supplier" :
                return redirect("business:suppliers_list")
            elif role == "Factory":
                return redirect("business:factories_list")
            elif role == "Dyeing Factory":
                return redirect("business:dyeing_factories_list")
        else:
            person = get_object_or_404(Person, owner=request.user, id = pk)
            form = PersonForm(request.POST, instance=person)
            return render(request, "business/parteners/person_detail.html", {"form": form})

class PersonDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        person = get_object_or_404(Person, owner=request.user, id = pk)
        person.delete()
        return redirect("business:home")


