from django.urls import path
from . import views
app_name = "business"

urlpatterns = [
    path("", views.home, name="home"),
]
