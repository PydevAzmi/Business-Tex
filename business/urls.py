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

    #Parteners
    path("customers/", views.PersonList.as_view(), name="customers_list"),
    path("suppliers/", views.PersonList.as_view(), name="suppliers_list"),
    path("factories/", views.PersonList.as_view(), name="factories_list"),
    path("dyeing-factories/", views.PersonList.as_view(), name="dyeing_factories_list"),
    path("customer/<pk>/", views.CustomerDetail.as_view(), name="customer_detail"),
    path("customer/<pk>/delete", views.CustomerDelete.as_view(), name="customer_delete"),
]
