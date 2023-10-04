
from autocare.models import SaleOrderPartModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer
from autocare.views.vehicle_part import VehiclePartModelSerializer
class SaleOrderPartModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    vehicle_part = VehiclePartModelSerializer(read_only=True)
    class Meta:
        model = SaleOrderPartModel
        fields = '__all__'

class SaleOrderPartModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """
    class Meta:
        model = SaleOrderPartModel
        fields = '__all__'

class SaleOrderPartViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SaleOrderPartModel.objects.all()
    serializer_class = SaleOrderPartModelSerializer
    create_serializer_class = SaleOrderPartModelCreateUpdateSerializer
    update_serializer_class = SaleOrderPartModelCreateUpdateSerializer
    filter_fields = {
        'vehicle_part': ['exact'],
        'sale_order': ['exact'],
    }
    search_fields = ['vehicle_part', 'sale_order',]
