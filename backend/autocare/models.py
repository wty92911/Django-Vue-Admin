from django.db import models
from django.db.models import Sum, UniqueConstraint
from django.utils import timezone
from dvadmin.utils.models import CoreModel

class EmployeeModel(CoreModel):
    '''
    员工
    '''
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名", unique=True, null=False, blank=False)
    TYPE_CHOICES = (
        (0, "老板"),
        (1, "管理"),
        (2, "员工")
    )
    employee_type = models.IntegerField(
        choices=TYPE_CHOICES, default=2, verbose_name="员工类型", null=True, blank=True, help_text="员工类型"
    )
    class Meta:
        db_table = "autocare_employee"
        verbose_name = '进货单表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
class CompanyModel(CoreModel):
    '''
    公司
    '''
    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, unique=True, help_text="电话")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名", unique=True, null=False, blank=False)
    class Meta:
        db_table = "autocare_company"
        verbose_name = '公司表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
    @property
    def total_real_price(self):
        return PurchaseOrderModel.objects.filter(company=self.id).aggregate(total_price=Sum('real_price'))['total_price'] or 0
class CustomerModel(CoreModel):

    mobile = models.CharField(max_length=255, verbose_name="电话", null=True, blank=True, help_text="电话")
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名", unique=True, null=False, blank=False)
    GENDER_CHOICES = (
        (0, "未知"),
        (1, "男"),
        (2, "女"),
    )
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=0, verbose_name="性别", null=True, blank=True, help_text="性别"
    )
    CUSTOMER_TYPES = (
        (0, "亲戚"),
        (1, "朋友"),
        (2, "一般客户")
    )
    customer_type = models.IntegerField(
        choices=CUSTOMER_TYPES, default=1, verbose_name="客户类型", null=True, blank=True, help_text="客户类型"
    )
    class Meta:
        db_table = "autocare_customer"
        verbose_name = '客户表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)



class VehicleModel(CoreModel):
    '''
    车辆
    '''
    plate_number = models.CharField(max_length=255, verbose_name="车牌号", null=True, blank=False, help_text="车牌号")
    customer = models.ForeignKey(
        to="CustomerModel",
        verbose_name="所属客户",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=False,
        blank=False,
        help_text="所属客户",
    )
    class Meta:
        db_table = "autocare_vehicle"
        verbose_name = '机动车表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
    @property
    def customer_name(self):
        return self.customer.name
    @property
    def customer_mobile(self):
        return self.customer.mobile
    
class VehiclePartModel(CoreModel):
    '''
    配件
    '''
    name = models.CharField(max_length=100, verbose_name="配件名", help_text="配件名", unique=True, null=False, blank=False)
    inventory_quantity = models.PositiveIntegerField(default=0, verbose_name="库存量", help_text="库存量")
    inventory_total_price = models.PositiveIntegerField(default=0, verbose_name="库存总额", help_text="库存总额")
    estimated_price = models.PositiveIntegerField(default=0, verbose_name="预估售价", help_text="预估售价")
    class Meta:
        db_table = "autocare_vehicle_part"
        verbose_name = '配件表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
    @property
    def inventory_average_price(self):
        return self.inventory_total_price // self.inventory_quantity
class SaleOrderModel(CoreModel):
    '''
    消费单
    '''
    total_price = models.PositiveIntegerField(default=0, verbose_name="总价格", help_text="总价格")
    real_price = models.PositiveIntegerField(default=0, verbose_name="实付价格", help_text="实付价格")
    discounted_price = models.PositiveIntegerField(default=0, verbose_name="优惠价格", help_text="优惠价格")
    datetime = models.TextField(default='', verbose_name="日期时间", help_text="日期时间")
    parts = models.TextField(default='', verbose_name="消费零件的json存储", help_text="消费零件的json存储")
    vehicle = models.ForeignKey(
        to="VehicleModel",
        verbose_name="消费车辆",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=False,
        blank=False,
        help_text="消费车辆",
    )

    employees = models.ManyToManyField(
        to="EmployeeModel",
        verbose_name="负责员工",
        default=1,
        db_constraint=False,
        null=False,
        blank=False,
        help_text="负责员工",
    )

    current_mile = models.PositiveIntegerField(default=0, verbose_name="当前里程", help_text="当前里程")
    #TODO: 一键筛选需要保养的车辆
    STATUS_CHOICES = (
        (0, "未完成"),
        (1, "已结算")
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES, default=0, verbose_name="消费单状态", null=False, blank=False, help_text="消费单状态"
    )
    payee = models.ForeignKey(
        default=0,
        to="EmployeeModel",
        verbose_name="收款人",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="收款人",
        related_name='payee'
    )
    PAY_METHOD_CHOICES = (
        (-1, ""),
        (0, "微信"),
        (1, "支付宝"),
        (2, "现金"),
    )
    pay_method = models.IntegerField(
        choices=PAY_METHOD_CHOICES, default=-1, verbose_name="支付方式", null=False, blank=False, help_text="支付方式"
    )
    class Meta:
        db_table = "autocare_sale_order"
        verbose_name = '消费单表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)

class PurchaseOrderPartModel(CoreModel):
    vehicle_part = models.ForeignKey(
        to='VehiclePartModel',
        verbose_name='配件',
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        help_text="配件",
    )
    purchase_order = models.ForeignKey(
        to='PurchaseOrderModel',
        verbose_name='采购单',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        help_text="采购单"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="数量", help_text="数量")
    average_price = models.PositiveIntegerField(default=0, verbose_name="单价", help_text="单价")
    total_price = models.PositiveIntegerField(default=0, verbose_name="总价", help_text="总价")
    class Meta:
        db_table = "autocare_purchase_order_part"
        verbose_name = '采购单配件表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)
        constraints = [
            UniqueConstraint(fields=['vehicle_part', 'purchase_order'], name='unique_vehicle_part_purchase_order')
        ]
class PurchaseOrderModel(CoreModel):
    '''
    采购单
    '''
    total_price = models.PositiveIntegerField(default=0, verbose_name="总价格", help_text="总价格")
    real_price = models.PositiveIntegerField(default=0, verbose_name="实付价格", help_text="实付价格")
    datetime = models.DateTimeField(default=None, verbose_name="日期时间", help_text="日期时间")
    supply_company = models.ForeignKey(
        to='CompanyModel',
        verbose_name='供应方',
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="供应方",
    )
    payer = models.ForeignKey(
        default=0,
        to="EmployeeModel",
        verbose_name="付款人",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="付款人",
        related_name='payer'
    )
    PAY_METHOD_CHOICES = (
        (-1, ""),
        (0, "微信"),
        (1, "支付宝"),
        (2, "现金"),
    )
    pay_method = models.IntegerField(
        choices=PAY_METHOD_CHOICES, default=-1, verbose_name="支付方式", null=False, blank=False, help_text="支付方式"
    )
    @property
    def parts(self):
        return PurchaseOrderPartModel.objects.filter(purchase_order=self.id)
    class Meta:
        db_table = "autocare_purchase_order"
        verbose_name = '采购单表'
        verbose_name_plural = verbose_name
        ordering = ('-create_datetime',)


