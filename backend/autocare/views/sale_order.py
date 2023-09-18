
from autocare.models import EmployeeModel
from autocare.models import SaleOrderModel
from rest_framework import serializers
from rest_framework.filters import BaseFilterBackend
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from autocare.views.vehicle import VehicleModelSerializer
from autocare.views.employee import EmployeeModelSerializer, EmployeeModelCreateUpdateSerializer

class SaleOrderModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    employees = EmployeeModelSerializer(many=True, read_only=True)
    # vehicle = VehicleModelSerializer(read_only=True)
    class Meta:
        model = SaleOrderModel
        fields = [
            'id', 'total_price', 'real_price', 'discounted_price', 'datetime',
            'vehicle', 'employees', 'current_mile', 'status', 'parts',
        ]

class SaleOrderModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    employees = serializers.PrimaryKeyRelatedField(many=True, queryset=EmployeeModel.objects.all())
    class Meta:
        model = SaleOrderModel
        fields = [
            'id', 'total_price', 'real_price', 'discounted_price', 'datetime',
            'vehicle', 'employees', 'current_mile', 'status',
            'parts',
        ]
class CustomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params
        if view.action == 'list':
            #TODO: 根据是否包含某个配件(VehiclePart)筛选订单 not (SaleVehiclePart)
            return queryset
        return queryset
class SaleOrderViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SaleOrderModel.objects.all()
    # filter_backends = [CustomFilter]
    serializer_class = SaleOrderModelSerializer
    create_serializer_class = SaleOrderModelCreateUpdateSerializer
    update_serializer_class = SaleOrderModelCreateUpdateSerializer
    filter_fields = {
        'vehicle': ['exact'],
        'status': ['exact'],
    }
    search_fields = ['vehicle', 'status']
