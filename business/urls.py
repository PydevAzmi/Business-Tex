from django.urls import path
from . import views
app_name = "business"

urlpatterns = [
    path("", views.home, name="home"),

    #Products
    path("yarn/", views.YarnList.as_view(), name="yarn_list"),
    path("yarn/<pk>/", views.YarnDetail.as_view(), name="Yarn_detail"),
    path("yarn/<pk>/delete", views.YarnDelete.as_view(), name="Yarn_delete"),
    path("fabric", views.FabricList.as_view(), name="fabric_list"),
    path("fabric/<pk>/", views.FabricDetail.as_view(), name="Fabric_detail"),
    path("fabric/<pk>/delete", views.FabricDelete.as_view(), name="fabric_delete"),

    
]
