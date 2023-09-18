from autocare.models import CompanyModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer


class CompanyModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = CompanyModel
        fields = "__all__"


class CompanyModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = CompanyModel
        fields = '__all__'



class CompanyViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CompanyModel.objects.all()
    serializer_class = CompanyModelSerializer
    create_serializer_class = CompanyModelCreateUpdateSerializer
    update_serializer_class = CompanyModelCreateUpdateSerializer
    # filter_fields = ['name', 'mobile']
    filter_fields = {
        "name": ["icontains"],
        "mobile": ["icontains"],
    }
    search_fields = ['name', 'mobile']
