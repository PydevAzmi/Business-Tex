from django import forms
from .models import *
from accounts.models import Person

class YarnForm(forms.ModelForm):
    class Meta:
        model = Yarn
        fields = ['name','yarn_type']


class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name','fabric_type']


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            "name",
            "email",
            "phone_number",
            "country",
            "city",
            "address",
            "address_2",
        ]

class YarnInvForm(forms.ModelForm):
    recieved_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    class Meta:
        model = YarnInventory
        fields = [
            "yarn",
            "supplier",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "recieved_at",
            "status",
            "located_at",
            "notes"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Person.objects.filter(owner=user, role='Supplier').all()
        self.fields['yarn'].queryset = Yarn.objects.filter(owner=user).all()

class SoldYarnForm(forms.ModelForm):
    sold_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    class Meta:
        model = SoldYarn
        fields =[
            "yarn_inventory",
            "customer",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "sold_at",
            "notes"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Person.objects.filter(owner=user, role='Customer').all()
        self.fields['yarn_inventory'].queryset = YarnInventory.objects.filter(owner=user).all()

# here i stopped
class FabricInvForm(forms.ModelForm):
    class Meta:
        model = FabricInventory
        fields = [
            "fabric",
            "yarn_factory",
            "supplier",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "quantity_recieved",
            "quantity_remaining",
            "quantity_out_dyeing",
            "quantity_buyied",
            "recieved_at",
            "located_at",
            "status",
            "notes"
        ]

 
class SoldFabricForm(forms.ModelForm):
    sold_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    class Meta:
        model = SoldFabric
        fields =[
            "fabric_dyeing_inventory",
            "Fabric_Inventory",
            "customer",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "sold_at",
            "notes"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Person.objects.filter(owner=user, role='Customer').all()
        self.fields['fabric_dyeing_inventory'].queryset = FabricDyeingInventory.objects.filter(owner=user).all()
        self.fields['Fabric_Inventory'].queryset = FabricInventory.objects.filter(owner=user).all()


class YarnFactoryCraeteForm(forms.ModelForm):
    orderd_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    class Meta:
        model =YarnFactory
        fields =[
            "yarn_inventory",
            "factory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "addons_yarn",
            "addons_weigth",
            "manufactured_fabric",
            "fabric_weight",
            "waste_ratio",
            "orderd_at",
            "notes"
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['yarn_inventory'].queryset = YarnInventory.objects.filter(owner=user).all()
        self.fields['factory'].queryset = Person.objects.filter(owner=user, role="Factory").all()
        self.fields['manufactured_fabric'].queryset = Fabric.objects.filter(owner=user).all()
        self.fields['addons_yarn'].queryset = Yarn.objects.filter(owner=user).all()

