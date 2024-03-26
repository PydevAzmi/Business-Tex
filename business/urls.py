from django.urls import path
from . import views
app_name = "business"

urlpatterns = [
    path("", views.home, name="home"),
    path("yarn", views.YarnList.as_view(), name="yarn_list"),
    path("fabric", views.FabricList.as_view(), name="fabric_list"),
]
