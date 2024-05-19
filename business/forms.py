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
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Person.objects.filter(owner=user, role='Supplier').all()
        self.fields['yarn'].queryset = Yarn.objects.filter(owner=user).all()

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


class FabricInvForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not kwargs.pop("instance", None):
            self.fields.pop('yarn_factory')
            self.fields.pop("quantity_buyied")
            self.fields.pop("quantity_out_dyeing")
            
        self.fields['fabric'].queryset = Fabric.objects.filter(owner=user).all()
        self.fields['supplier'].queryset = Person.objects.filter(owner=user, role__in=['Supplier', 'Factory'] ).all()

    recieved_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
        }))
    
    class Meta:
        model = FabricInventory
        fields = [
            "fabric",
            "supplier",
            "yarn_factory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "quantity_recieved",
            "quantity_remaining",
            "quantity_buyied",
            "quantity_out_dyeing",
            "recieved_at",
            "located_at",
            "status",
            "notes"
        ]


class SoldFabricForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['customer'].queryset = Person.objects.filter(owner=user, role='Customer').all()
        self.fields['fabric_dyeing_inventory'].queryset = FabricDyeingInventory.objects.filter(owner=user).all()
        self.fields['Fabric_Inventory'].queryset = FabricInventory.objects.filter(owner=user).all()

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


class YarnFactoryCraeteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['yarn_inventory'].queryset = YarnInventory.objects.filter(owner=user).all()
        self.fields['factory'].queryset = Person.objects.filter(owner=user, role="Factory").all()
        self.fields['manufactured_fabric'].queryset = Fabric.objects.filter(owner=user).all()
        self.fields['addons_yarn'].queryset = Yarn.objects.filter(owner=user).all()

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


class FabricDyeingInventoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not kwargs.pop("instance", None):
            self.fields.pop('fabric_dyeing_factory')
            self.fields.pop("quantity_buyied")
        self.fields['fabric'].queryset = Fabric.objects.filter(owner=user).all()
        self.fields['supplier'].queryset = Person.objects.filter(owner=user, role__in=['Supplier', 'Dyeing Factory'] ).all()
    
    recieved_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
        }))
       
    class Meta:
        model = FabricDyeingInventory
        fields = [
            "fabric",
            "supplier",
            "fabric_dyeing_factory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "unit_price",
            "total_price",
            "added_tax",
            "discount",
            "quantity_recieved",
            "quantity_remaining",
            "quantity_buyied",
            "recieved_at",
            "located_at",
            "status",
            "notes",

        ]


class FabricDyeingFactoryForm(forms.ModelForm):
    came_out_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
        }))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['fabric_inv'].queryset = FabricInventory.objects.filter(owner=user).all()
        self.fields['dyeing_factory'].queryset = Person.objects.filter(owner=user, role="Dyeing Factory").all()

    class Meta:
        model = FabricDyeingFactory
        fields =[
            "fabric_inv",
            "dyeing_factory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "came_out_at",
            "notes"
        ]


class ReturnedYarnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['yarn_factory'].queryset = YarnFactory.objects.filter(yarn_inventory__owner=user).all()

    returned_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    
    class Meta:
        model = ReturnedYarn
        fields = [
            "yarn_factory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "returned_at",
            "status",
            "notes",
        ]


class ReturnedFabricForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['fabric_inventory'].queryset = FabricInventory.objects.filter(owner=user).all()

    returned_at = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "id": "datePickerFormat",
            }))
    
    class Meta:
        model = ReturnedFabric
        fields =[
            "fabric_inventory",
            "total_weight",
            "unit_type",
            "quantity_per_unit",
            "returned_at",
            "status",
            "notes",
        ]
