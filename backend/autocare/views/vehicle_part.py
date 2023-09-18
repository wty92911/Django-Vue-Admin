from rest_framework import serializers
from autocare.models import VehiclePartModel
from rest_framework.filters import BaseFilterBackend
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer


class VehiclePartModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    inventory_average_price = serializers.IntegerField(required=False)
    
    class Meta:
        model = VehiclePartModel
        fields = "__all__"


class VehiclePartModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = VehiclePartModel
        fields = '__all__'
    def validate(self, data):
        if data.get('estimated_price', 0) <= (data.get('inventory_total_price',1) / data.get('inventory_quantity', 1)):
            raise serializers.ValidationError("预估单价必须大于库存均价")
        return super().validate(data)


class CustomFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        params = request.query_params
        if view.action == 'list':
            if int(params.get('inventory_quantity', -1)) >= 0:
                return queryset.filter(inventory_quantity__lte=int(params.get('inventory_quantity', -1)))
            return queryset
        return None
class VehiclePartViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = VehiclePartModel.objects.all()
    filter_backends = [CustomFilter]
    serializer_class = VehiclePartModelSerializer
    create_serializer_class = VehiclePartModelCreateUpdateSerializer
    update_serializer_class = VehiclePartModelCreateUpdateSerializer
    # filter_fields = ['name', 'mobile']
    filter_fields = {
        "name": ["icontains"],
    }
    search_fields = ["name"]
