from django.urls import path
from . import views
app_name = "business"

urlpatterns = [
    #Dashboard
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
    path("dyeing/", views.PersonList.as_view(), name="dyeing_list"),
    path("person/<pk>/", views.PersonDetail.as_view(), name="Person_detail"),
    path("person/<pk>/delete", views.PersonDelete.as_view(), name="person_delete"),

    #Sales
    path("inventory/yarn-in/", views.YarnInvList.as_view(), name="yarn_inv_list"),
    path("inventory/yarn-in/<pk>/", views.YarnInvDetail.as_view(), name="YarnInventory_detail"),
    path("inventory/yarn-in/<pk>/delete", views.YarnInvDelete.as_view(), name="yarn_inv_delete"),
    path("inventory/yarn-out/", views.SoldYarnList.as_view(), name="yarn_out_list"),
    path("inventory/yarn-out/<pk>/", views.SoldYarnDetail.as_view(), name="SoldYarn_detail"),
    path("inventory/yarn-out/<pk>/delete", views.SoldYarnDelete.as_view(), name="yarn_out_delete"),

    path("inventory/fabric-in/", views.FabricInvList.as_view(), name="fabric_inv_list"),
    path("inventory/fabric-in/<pk>/", views.FabricInvDetail.as_view(), name="FabricInventory_detail"),
    path("inventory/fabric-in/<pk>/delete", views.FabricInvDelete.as_view(), name="fabric_inv_delete"),

    path("inventory/dyied-fabric/", views.DyeidFabricInvList.as_view(), name="dyied_fabric_inv_list"),
    path("inventory/dyied-fabric/<pk>/", views.DyeidFabricInvDetail.as_view(), name="FabricDyeingFactory_detail"),
    path("inventory/dyied-fabric/<pk>/delete", views.DyeidFabricInvDelete.as_view(), name="dyied_fabric_inv_delete"),
    
    path("inventory/fabric-out/", views.SoldFabricList.as_view(), name="fabric_out_list"),
    path("inventory/fabric-out/<pk>/", views.SoldFabricDetail.as_view(), name="SoldFabric_detail"),
    path("inventory/fabric-out/<pk>/delete", views.SoldFabricDelete.as_view(), name="fabric_out_delete"),

    #Manufacturing  
    path("manufacture/yarn-factory/", views.YarnFactoryList.as_view(), name ="yarn_factory_list"),
    path("manufacture/yarn-factory/<pk>/", views.YarnFactoryDetail.as_view(), name ="YarnFactory_detail"),
    path("manufacture/yarn-factory/<pk>/delete", views.YarnFactoryDelete.as_view(), name ="yarn_factory_delete"),
]
