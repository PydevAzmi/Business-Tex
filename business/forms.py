from django import forms
from .models import *


class YarnForm(forms.ModelForm):
    class Meta:
        model = Yarn
        fields = ['name','yarn_type']


class FabricForm(forms.ModelForm):
    class Meta:
        model = Fabric
        fields = ['name','fabric_type']