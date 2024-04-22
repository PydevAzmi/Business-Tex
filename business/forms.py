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