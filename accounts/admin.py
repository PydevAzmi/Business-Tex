from django.contrib import admin
from .models import User, Person, Company
# Register your models here.

admin.site.register(User)
admin.site.register(Person)
admin.site.register(Company)