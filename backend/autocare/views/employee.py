from rest_framework import serializers
from autocare.models import EmployeeModel
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.serializers import CustomModelSerializer


class EmployeeModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    class Meta:
        model = EmployeeModel
        fields = "__all__"


class EmployeeModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = EmployeeModel
        fields = '__all__'



class EmployeeViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = EmployeeModel.objects.all()
    serializer_class = EmployeeModelSerializer
    create_serializer_class = EmployeeModelCreateUpdateSerializer
    update_serializer_class = EmployeeModelCreateUpdateSerializer
    # filter_fields = ['name', 'mobile']
    filter_fields = {
        "name": ["icontains"],
        "employee_type": ["exact"],
    }
    search_fields = ["name"]
