from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *
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
        return render(request, "business/products/list_fabric.html", {'fabric_list': fabric_list, "form": form}) 

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
        elif path == "/dyeing/":
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
            elif path == "/dyeing/":
                myform.role = "Dyeing Factory"
                myform.save()
                return redirect("business:dyeing_list")
                            
        
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
                return redirect("business:dyeing_list")
        return render(request, "business/parteners/person_detail.html", {"form": form})


class PersonDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        person = get_object_or_404(Person, owner=request.user, id = pk)
        role =  person.role
        person.delete()
        if role == "Customer" :
            return redirect("business:customers_list")
        elif role == "Supplier" :
            return redirect("business:suppliers_list")
        elif role == "Factory":
            return redirect("business:factories_list")
        elif role == "Dyeing Factory":
            return redirect("business:dyeing_list")


class YarnInvList(LoginRequiredMixin, View):
    def get(self, request):
        form = YarnInvForm(user=request.user)
        yarn_list = YarnInventory.objects.filter(owner=request.user).all()
        return render(request, "business/sales/yarn/yarn_inv_list.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        form = YarnInvForm(request.POST, user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:yarn_inv_list")


class YarnInvDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        yarn = get_object_or_404(YarnInventory, owner = request.user, id=pk)
        form = YarnInvForm(user=request.user, instance = yarn)
        return render(request, "business/sales/yarn/yarn_inv_detail.html", {"form":form})

    def post(self, request, pk):
        yarn = get_object_or_404(YarnInventory, owner=request.user, id=pk)
        form = YarnInvForm(request.POST, user=request.user, instance = yarn)
        if form.is_valid():
            form.save()
            return redirect("business:yarn_inv_list")
        return render(request, "business/sales/yarn/yarn_inv_detail.html", {"form":form})


class YarnInvDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        yarn_inv = get_object_or_404(YarnInventory, owner=request.user, id=pk)
        yarn_inv.delete()
        return redirect("business:yarn_inv_list")


class SoldYarnList(LoginRequiredMixin, View):
    def get(self, request):
        form = SoldYarnForm(user=request.user)
        yarn_list = SoldYarn.objects.filter(owner=request.user).all()
        return render(request, "business/sales/yarn/yarn_out_list.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        form = SoldYarnForm(request.POST, user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            exist = myform.yarn_inventory.get_existing_weight()
            print( myform.total_weight <= 0 and myform.total_weight > exist)
            if myform.total_weight <= 0 or myform.total_weight > exist :
                yarn_list = SoldYarn.objects.filter(owner=request.user).all()
                form.add_error(None, "The Total Weight Must Be Less Than The Actual Existing Weight.")
                return render(request, "business/sales/yarn/yarn_out_list.html", {'yarn_list': yarn_list, "form": form})
            myform.save()
        return redirect("business:yarn_out_list")


class SoldYarnDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        yarn = get_object_or_404(SoldYarn, owner = request.user, id=pk)
        form = SoldYarnForm(user=request.user, instance = yarn)
        return render(request, "business/sales/yarn/yarn_out_detail.html", {"form":form})

    def post(self, request, pk):
        yarn = get_object_or_404(SoldYarn, owner=request.user, id=pk)
        form = SoldYarnForm(request.POST, user=request.user, instance = yarn)
        last_total = yarn.total_weight
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            exist = myform.yarn_inventory.get_existing_weight()
            print(last_total)
            if myform.total_weight < 0 or myform.total_weight > exist + last_total:
                form.add_error(None, "The Total Weight Must Be Less Than The Actual Existing Weight.")
                return render(request, "business/sales/yarn/yarn_out_detail.html", {"form": form})
            myform.save()
        return render(request, "business/sales/yarn/yarn_inv_detail.html", {"form":form})

    
class SoldYarnDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        sold_yarn = get_object_or_404(SoldYarn, owner=request.user, id=pk)
        sold_yarn.delete()
        return redirect("business:yarn_out_list")


class SoldFabricList(LoginRequiredMixin, View):
    def get(self, request):
        form = SoldFabricForm(user=request.user)
        fabric_list = SoldFabric.objects.filter(owner=request.user).all()
        return render(request, "business/sales/raw_fabric/fabric_out_list.html", {'fabric_list': fabric_list, "form": form})

    def post(self, request):
        form = SoldFabricForm(request.POST, user=request.user)
        fabric_list = SoldFabric.objects.filter(owner=request.user).all()
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            if myform.Fabric_Inventory and myform.fabric_dyeing_inventory :
                form.add_error(None, "You Must Select Only One Kind of Fabric!")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", {'fabric_list': fabric_list, "form": form})
            elif myform.Fabric_Inventory:
                exist = myform.Fabric_Inventory.get_existing_weight()
            elif myform.fabric_dyeing_inventory:
                exist = myform.fabric_dyeing_inventory.get_existing_weight()
            else:
                form.add_error(None, "You Must Select At Least One Fabric!")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", {'fabric_list': fabric_list, "form": form})

            total = myform.total_weight
            if total <= 0 or total > exist :
                form.add_error(None, "The Total Weight Must Be Less Than The Actual Existing Weight.")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", {'fabric_list': fabric_list, "form": form})
            myform.save()
        return redirect("business:fabric_out_list")


class SoldFabricDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        fabric = get_object_or_404(SoldFabric, owner = request.user, id=pk)
        form = SoldFabricForm(user=request.user, instance = fabric)
        return render(request, "business/sales/raw_fabric/fabric_out_detail.html", {"form":form})

    def post(self, request, pk):
        fabric = get_object_or_404(SoldFabric, owner=request.user, id=pk)
        last_total = fabric.total_weight
        form = SoldFabricForm(request.POST, user=request.user, instance = fabric)
        if form.is_valid():
            myform = form.save(commit=False)
            if myform.Fabric_Inventory:
                exist = myform.Fabric_Inventory.get_existing_weight() 
            elif myform.fabric_dyeing_inventory:
                exist = myform.fabric_dyeing_inventory.get_existing_weight()
            elif myform.Fabric_Inventory and myform.fabric_dyeing_inventory :
                form.add_error(None, "You Must Select Only One Kind of Fabric!")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", { "form": form})
            else:
                form.add_error(None, "You Must Select At Least One Fabric!")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", { "form": form})
            total = myform.total_weight
            if total < 0 or total > exist + last_total :
                form.add_error(None, "The Total Weight Must Be Less Than The Actual Existing Weight.")
                return render(request, "business/sales/raw_fabric/fabric_out_list.html", {"form": form})
            myform.save()
            return redirect("business:fabric_out_list")
        return render(request, "business/sales/raw_fabric/fabric_out_detail.html", {"form":form})

    
class SoldFabricDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        sold_fabric = get_object_or_404(SoldFabric, owner=request.user, id=pk)
        sold_fabric.delete()
        return redirect("business:fabric_out_list")
 
class FabricInvList(LoginRequiredMixin, View):
    def get(self, request):
        form = FabricInvForm(user=request.user)
        fabric_list = FabricInventory.objects.filter(owner= request.user).all()
        return render(request, "business/sales/raw_fabric/fabric_inv_list.html", {"fabric_list": fabric_list, "form":form})

    def post(self, request):
        form = FabricInvForm(request.POST, user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:fabric_inv_list")

class FabricInvDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        fabric = get_object_or_404(FabricInventory, owner = request.user, id=pk)
        form = FabricInvForm(user=request.user, instance = fabric)
        return render(request, "business/sales/raw_fabric/fabric_inv_detail.html", {"form":form})

    def post(self, request, pk):
        fabric = get_object_or_404(FabricInventory, owner=request.user, id=pk)
        form = FabricInvForm(request.POST, user=request.user, instance = fabric)
        if form.is_valid():
            form.save()
            return redirect("business:yarn_inv_list")
        return render(request, "business/sales/yarn/yarn_inv_detail.html", {"form":form})


class FabricInvDelete(LoginRequiredMixin,View):
    def post(self, request, pk):
        fabric_inv = get_object_or_404(FabricInventory, owner=request.user, id=pk)
        fabric_inv.delete()
        return redirect("business:fabric_inv_list")
    

class DyeidFabricInvList(LoginRequiredMixin, View):
    def get(self, request):
        form = FabricDyeingInventoryForm(user=request.user)
        fabric_list = FabricDyeingInventory.objects.filter(owner= request.user).all()
        return render(request, "business/sales/dyied_fabric/dyied_fabric_inv_list.html", {"fabric_list": fabric_list, "form":form})

    def post(self, request):
        form = FabricDyeingInventoryForm(request.POST, user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.owner = request.user
            myform.save()
        return redirect("business:dyied_fabric_inv_list")


class DyeidFabricInvDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        dyied_fabric = get_object_or_404(FabricDyeingInventory, owner = request.user, id=pk)
        form = FabricDyeingInventoryForm(user=request.user, instance = dyied_fabric)
        return render(request, "business/sales/raw_fabric/fabric_inv_detail.html", {"form":form})

    def post(self, request, pk):
        dyied_fabric = get_object_or_404(FabricDyeingInventory, owner=request.user, id=pk)
        form = FabricDyeingInventoryForm(request.POST, user=request.user, instance = dyied_fabric)
        if form.is_valid():
            form.save()
            return redirect("business:dyied_fabric_inv_list")
        return render(request, "business/sales/yarn/fabric_inv_detail.html", {"form":form})


class DyeidFabricInvDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        dyeid_fabric = get_object_or_404(FabricDyeingInventory,owner = request.user, id= pk)
        dyeid_fabric.delete()
        return redirect("business:dyied_fabric_inv_list")


class YarnFactoryList(LoginRequiredMixin, View):
    def get(self, request):
        form = YarnFactoryCraeteForm(user = request.user)
        yarn_list = YarnFactory.objects.filter(yarn_inventory__owner = request.user).all()
        return render(request, "business/Manufacturing/yarn_factory_list.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        form = YarnFactoryCraeteForm(request.POST, user=request.user)
        if form.is_valid():
            myform = form.save(commit=False)
            exist = myform.yarn_inventory.get_existing_weight()
            if myform.total_weight <= 0 or myform.total_weight > exist :
                yarn_list = YarnFactory.objects.filter(yarn_inventory__owner = request.user).all()
                form.add_error(None, "The Total Weight Must Be Less Than The Actual Existing Weight.")
                return render(request, "business/Manufacturing/yarn_factory_list.html", {'yarn_list': yarn_list, "form": form})
            myform.save()
        return redirect("business:yarn_factory_list")

class YarnFactoryDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        yarn_factory = get_object_or_404(YarnFactory, id =pk)
        form = YarnFactoryCraeteForm( user= request.user, instance = yarn_factory)
        return render(request, "business/Manufacturing/yarn_factory_detail.html", {"form" : form})
    
    def post(self, request, pk):
        yarn_factory = get_object_or_404(YarnFactory, id=pk)
        form = YarnFactoryCraeteForm(request.POST, user=request.user, instance = yarn_factory)
        if form.is_valid():
            form.save()
            return redirect("business:yarn_factory_list")
        return render(request, "business/Manufacturing/yarn_factory_detail.html", {"form" : form})


class YarnFactoryDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        yarn_factory = get_object_or_404(YarnFactory, yarn_inventory__owner =request.user, id =pk)
        yarn_factory.delete()
        return redirect("business:yarn_factory_list")


class FabricDyeingFactoryList(LoginRequiredMixin, View):
    def get(self, request):
        form = FabricDyeingFactoryForm(user = request.user)
        yarn_list = FabricDyeingFactory.objects.filter(fabric_inv__owner = request.user).all()
        return render(request, "business/Manufacturing/yarn_factory_list.html", {'yarn_list': yarn_list, "form": form})

    def post(self, request):
        pass


class FabricDyeingFactoryDetail(LoginRequiredMixin, View):
    def get(self, request, pk):
        fabricdyeingfactory = get_object_or_404(FabricDyeingFactory, id =pk)
        form = FabricDyeingFactoryForm(user= request.user, instance = fabricdyeingfactory)
        return render(request, "business/Manufacturing/yarn_factory_detail.html", {"form" : form})

    def post(self, request, pk):
        pass


class FabricDyeingFactoryDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        yarn_factory = get_object_or_404(YarnFactory, fabric_inv__owner =request.user, id =pk)
        yarn_factory.delete()
        return redirect("business:yarn_factory_list")


