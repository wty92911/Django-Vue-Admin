
from autocare.models import EmployeeModel
from autocare.models import PurchaseOrderModel
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from autocare.views.company import CompanyModelSerializer
from autocare.views.employee import EmployeeModelSerializer
from autocare.views.purchase_order_part import PurchaseOrderPartModelSerializer
class PurchaseOrderModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    parts = PurchaseOrderPartModelSerializer(read_only=True, many=True)
    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'

class PurchaseOrderModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = PurchaseOrderModel
        fields = '__all__'

class PurchaseOrderViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = PurchaseOrderModel.objects.all()
    serializer_class = PurchaseOrderModelSerializer
    create_serializer_class = PurchaseOrderModelCreateUpdateSerializer
    update_serializer_class = PurchaseOrderModelCreateUpdateSerializer
    filter_fields = {
        'supply_company': ['exact'],
        'payer': ['exact'],
    }
    search_fields = ['supply_company', 'payer',]
