from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from allauth.account.forms import SignupForm
from django import forms
from .models import User
from django.contrib.auth.forms import UserChangeForm

custom_user = get_user_model()

class CustomUserCreationForm(SignupForm):
    phone_number = forms.CharField(
        min_length=11, 
        max_length=13, 
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Phone",
            "id": "hourDomesticMask"
            }),
        label=_("Phone Number")
    )

    def save(self, request):
        # Save the user using the super method
        user = super(CustomUserCreationForm, self).save(request)
        # Update the user's phone number
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user
    
    class Meta:
        model = custom_user
        fields = (
            "email",
            "username",
            "phone_number",
        )

class CuatomUserChangeForm(forms.ModelForm):
    email = forms.CharField(disabled=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email', 'username', 'phone_number', 'wa_phone', 'profile_image',
            
            ]
        widgets = {
            'profile_image': forms.FileInput(attrs={
            "id": "inputGroupFile02",
            "class":"form-control",
            }),
        }