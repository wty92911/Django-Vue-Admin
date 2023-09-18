from django.urls import path
from rest_framework import routers
from autocare.views.vehicle import VehicleViewSet
from autocare.views.company import CompanyViewSet
from autocare.views.customer import CustomerViewSet
from autocare.views.employee import EmployeeViewSet
from autocare.views.sale_order import SaleOrderViewSet
from autocare.views.vehicle_part import VehiclePartViewSet
from autocare.views.purchase_order import PurchaseOrderViewSet
from autocare.views.purchase_order_part import PurchaseOrderPartViewSet
system_url = routers.SimpleRouter()
system_url.register(r'vehicle', VehicleViewSet)
system_url.register(r'company', CompanyViewSet)
system_url.register(r'employee', EmployeeViewSet)
system_url.register(r'customer', CustomerViewSet)
system_url.register(r'sale_order', SaleOrderViewSet)
system_url.register(r'vehicle_part', VehiclePartViewSet)
system_url.register(r'purchase_order', PurchaseOrderViewSet)
system_url.register(r'purchase_order_part', PurchaseOrderPartViewSet)
urlpatterns = [
]
urlpatterns += system_url.urls
