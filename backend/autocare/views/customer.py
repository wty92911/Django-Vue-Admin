from autocare.models import CustomerModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer


class CustomerModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = CustomerModel
        fields = "__all__"


class CustomerModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = CustomerModel
        fields = '__all__'



class CustomerViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CustomerModel.objects.all()
    serializer_class = CustomerModelSerializer
    create_serializer_class = CustomerModelCreateUpdateSerializer
    update_serializer_class = CustomerModelCreateUpdateSerializer
    # filter_fields = ['name', 'mobile']
    filter_fields = {
        "name": ["icontains"],
        "mobile": ["icontains"],
        "gender": ["icontains"],
        "customer_type": ["exact"],
    }
    search_fields = ['name', 'mobile']
