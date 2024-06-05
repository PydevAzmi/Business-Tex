from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CuatomUserChangeForm
# Create your views here.

@login_required
def profile_edit(request):
    user = request.user
    user_form = CuatomUserChangeForm(instance= user)

    if request.method == "POST":
        user_form = CuatomUserChangeForm(request.POST, request.FILES, instance = user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect(reverse('accounts:user_info'))
    context= {
        "form" : user_form
    }
    return render(request, "account/user_info.html", context)

