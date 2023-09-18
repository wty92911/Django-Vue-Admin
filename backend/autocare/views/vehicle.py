from rest_framework import serializers
from autocare.models import VehicleModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer


class VehicleModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    customer_name = serializers.ReadOnlyField()
    customer_mobile = serializers.ReadOnlyField()
    class Meta:
        model = VehicleModel
        fields = "__all__"


class VehicleModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = VehicleModel
        fields = '__all__'



class VehicleViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer
    create_serializer_class = VehicleModelCreateUpdateSerializer
    update_serializer_class = VehicleModelCreateUpdateSerializer
    # filter_fields = ['name', 'mobile']
    filter_fields = {
        "plate_number": ["icontains"],
        "customer": ["exact"],
    }
    search_fields = ["plate_number", "customer"]
