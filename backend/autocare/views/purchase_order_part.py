
from autocare.models import PurchaseOrderPartModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from autocare.views.vehicle_part import VehiclePartModelSerializer
class PurchaseOrderPartModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    vehicle_part = VehiclePartModelSerializer(read_only=True)
    class Meta:
        model = PurchaseOrderPartModel
        fields = '__all__'

class PurchaseOrderPartModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = PurchaseOrderPartModel
        fields = '__all__'

class PurchaseOrderPartViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = PurchaseOrderPartModel.objects.all()
    serializer_class = PurchaseOrderPartModelSerializer
    create_serializer_class = PurchaseOrderPartModelCreateUpdateSerializer
    update_serializer_class = PurchaseOrderPartModelCreateUpdateSerializer
    filter_fields = {
        'vehicle_part': ['exact'],
        'purchase_order': ['exact'],
    }
    search_fields = ['vehicle_part', 'purchase_order',]
