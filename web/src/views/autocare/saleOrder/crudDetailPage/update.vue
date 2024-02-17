<template>
  <d2-container :class="{ 'page-compact': true }">
    <el-main>
    <el-form :model="sale_order" :rules="rules" ref="sale_order" >
      <el-form-item label="当前时间" prop="datetime">
        <el-date-picker
          v-model="sale_order.datetime"
          type="datetime"
          style="margin: auto"
          
          placeholder="选择日期时间">
        </el-date-picker>
      </el-form-item>
      <el-form-item label="负责人员" prop="employees">
        <el-select 
          v-model="sale_order.employees"
          value-key="name" 
          filterable multiple
          style="margin: auto"
          placeholder="请派工" >
          <el-option
            v-for="item in all_employees"
            :key="item.id"
            :label="item.name"
            :value="item">
          </el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="参考总价" prop="total_price">
        <el-input
          v-model="sale_order.total_price"
          style="width: 10%; margin-left: 10px; font-weight: bold; margin-right: 10px;"
          placeholder="消费单总价"
          prefix-icon="el-icon-coin"
          readonly
        ></el-input>
      </el-form-item>
      <el-form-item label="车辆信息">
        <el-row :gutter="20">
          <el-col :span="4">
            <el-form-item prop="vehicle">
              <el-select 
                v-model="sale_order.vehicle"
                value-key="plate_number" 
                style="width: 100%;"
                filterable placeholder="请输入或选择车牌号" >
                <el-option
                  v-for="item in all_vehicles"
                  :key="item.id"
                  :label="item.plate_number"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
         
          <el-col :span="4">
            <el-form-item  prop="current_mile"  >
              <el-input label="进店里程"
                v-model="sale_order.current_mile"
                prefix-icon="el-icon-ship"
                placeholder="进店里程" >
              <i slot="suffix" style="font-style: normal; margin-right: 10px">KM</i>
              </el-input>
            </el-form-item>
          </el-col>
         
          <el-col :span="4"> 
            <el-form-item >
              <el-input
                v-model="sale_order.vehicle.customer_name"
                placeholder="车主姓名"
                style="margin:auto"
                prefix-icon="el-icon-s-custom"
                disabled>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item >
              <el-input
                v-model="sale_order.vehicle.customer_mobile"
                placeholder="车主电话"
                prefix-icon="el-icon-mobile-phone"
                disabled>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form-item>
      
      <el-form-item label="结算信息">
        <el-row :gutter="20">
          <el-col :span="4">
            <el-switch v-model.number="sale_order.status" :active-value="Number(1)" :inactive-value="Number(0)" active-color="#13ce66" active-text="已结算" inactive-text="待结算" @change="handleSwitchChange"/>
          </el-col>
          <el-col :span="4">
            <el-form-item prop="payee" v-if="sale_order.status === 1">
              <el-select 
                v-model="sale_order.payee"
                value-key="id" 
                filterable placeholder="请选择收款人" >
                <el-option
                  v-for="item in filteredEmployees"
                  :key="item.id"
                  :label="item.name"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item prop="pay_method" v-if="sale_order.status === 1">
              <el-select
                v-model="sale_order.pay_method"
                value-key="id" 
                filterable placeholder="请选择收款方式" >
                <el-option
                  v-for="item in all_pay_methods"
                  :key="item.id"
                  :label="item.name"
                  :value="item">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item  prop="real_price" v-if="sale_order.status === 1">
              <el-input v-if="sale_order.status === 1" 
                v-model="sale_order.real_price"
                placeholder="请输入实收金额">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form-item> 
      <el-table  :data="sale_order.parts" style="margin-top: 20px; width: 100%">
        <el-table-column label="序号" min-width="5%">
          <template slot-scope="scope">
          {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column label="配件名称" min-width="30%">
          <template slot-scope="scope">
            <el-select
              v-model="scope.row.vehicle_part"
              value-key="name" 
              style="width: 100%;"
              filterable placeholder="请输入或选择配件" 
              @change="handlePartSelectClick">
              <el-option
                v-for="item in all_vehicle_parts"
                :key="item.id"
                :label="item.name"
                :value="item">
              </el-option>
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="参考单价(元)" min-width="10%">
          <template slot-scope="scope">
            <el-input
              v-model="scope.row.vehicle_part.estimated_price"
              placeholder=""
              disabled
            ></el-input>
          </template>
        </el-table-column>
        <el-table-column label="配件数量(个)" min-width="20%">
          <template slot-scope="scope">
            <el-input-number
              v-model="scope.row.quantity"
              :min="1"
              :max="20"
              style="width:100%; display: flex; align-items: center;"
            ></el-input-number>
          </template>
        </el-table-column>
        <el-table-column label="实际单价(元)" min-width="10%">
          <template slot-scope="scope">
            <el-input
              v-model="scope.row.average_price"
              style="width: 100%;"
              placeholder="">
          </el-input>
          </template>
        </el-table-column>
        <el-table-column label="总价(元)" min-width="15%" >
            <template slot-scope="scope">
              <!-- {{calcTotalPrice(scope.row)}} -->
              <!-- {{ totalPrice(scope.row) }} -->
              {{ handleNaN(scope.row.total_price) }}
              <!-- <el-input v-model="scope.row.total_price"  disabled></el-input> -->
          </template>
        </el-table-column>
        <el-table-column min-width="10%">
          <template slot-scope="scope">
            <el-button
              @click.prevent="removePart(scope.row)"
              type="danger"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-form-item>
        <div style="display: flex; justify-content: space-between;">
          <el-button
            @click="addPart"
            type="primary"
            style="margin-top: 10px;"
          >新增销售配件</el-button>
          <el-button
            @click="handleButtonSave"
            type="success"
            style="margin-top: 10px; width: 10%;"
          >保存消费单</el-button>
        </div>
      </el-form-item>
    </el-form>
    </el-main>
  </d2-container>
</template>
<script>
import { GetVehicles, GetVehicleParts, GetEmployees, GetOrderPart, DelOrderPart, UpdateOrderPart, AddOrderPart} from './api'
import { AddObj as AddSaleOrder, UpdateObj as UpdateSaleOrder} from '../api'
import { mapState, mapActions } from 'vuex'
export default {
  name: 'saleOrderUpdatePage',
  data () {
    return {
      type: 'update',
      sale_order: {
        id: null,
        current_mile: '',
        datetime: new Date(),
        discounted_price: null,
        employees: null,
        parts: [
            {
              id: null,
              vehicle_part: {
                id: '',
                name: '',
                estimated_price: 0,
              },
              quantity: 1,
              average_price: null,
              total_price: 0,
            }
        ],
        payee: null,
        pay_method: null,
        real_price: null,
        status: 0,
        total_price: null,
        vehicle: {
            customer_name: '',
            customer_mobile: '',
        },
      },
      rules : {
        current_mile: [
          { required: true, message: '请输入进店里程数', trigger: 'blur' },
          { pattern: /^[1-9][1-9]*$/, message: "里程必须为正整数", trigger: 'blur' }
        ],
        employees: [
          { required: true, message: '请至少选择一名负责人员', trigger: 'blur' }
        ],
        vehicle: [
          { required: true, message: '请选择或选择车牌号', trigger: 'blur' }
        ],
        payee: [
          { required: true, message: '请选择收款人', trigger: 'blur' }
        ],
        pay_method: [
          { required: true, message: '请选择收款方式', trigger: 'blur' }
        ],
        real_price: [
          { required: true, message: '请输入收款金额', trigger: 'blur' },
          { pattern: /^[1-9][1-9]*$/, message: "收款金额必须为正整数", trigger: 'change' }
        ],
      },
      all_employees: [],
      all_vehicle_parts: [],
      all_vehicles: [],
    };
  },
  created() {
    // 使用 Promise.all 等待多个异步操作完成
    Promise.all([
      this.getVehicles(),
      this.getVehicleParts(),
      this.getEmployees()
    ]).then(([vehiclesData, vehiclePartsData, employeesData]) => {
      // 将获取的数据分别赋值给相应的属性
      this.all_vehicles = vehiclesData;
      this.all_vehicle_parts = vehiclePartsData;
      this.all_employees = employeesData;
      this.loadSaleOrderData();
    });
    this.all_pay_methods = [
      {
        "id": 0, "name": "微信",
      },
      {
        "id": 1, "name": "支付宝",
      },
      {
        "id": 2, "name": "现金",
      },
    ]
  },
  mounted() {
    // console.log(this.sale_order.status);
  },
  computed: {
    handleNaN() {
      return (num) => isNaN(num) ? "请先输入实际单价" : num;
    },
    filteredEmployees() {
      return this.all_employees.filter(item => item.employee_type === 0 || item.employee_type === 1);
    }
  },
  watch: {
    'sale_order.parts': {
      deep: true,
      handler(newVal, oldVal) {
        this.updateTotalPrice(newVal, oldVal)
      }
    }
  },
  methods: {
    ...mapActions('d2admin/page', [
      'close',
      'closeThis',
    ]),
    loadSaleOrderData() {
      this.sale_order = { ...this.$route.params.sale_order };
      this.sale_order.vehicle = this.all_vehicles.find(vehicle => vehicle.id === this.sale_order.vehicle);
      this.sale_order.payee = this.all_employees.find(emp => emp.id === this.sale_order.payee);
      this.sale_order.pay_method = this.all_pay_methods.find(mtd => mtd.id === this.sale_order.pay_method);
      this.sale_order.datetime = new Date(this.sale_order.datetime);
      
      console.log(this.sale_order);
      
    },
    updateTotalPrice(newVal, oldVal) {
      const selectedParts = this.sale_order.parts.map(item => item.vehicle_part.name);
      const duplicatePart = selectedParts.find(name => selectedParts.indexOf(name) !== selectedParts.lastIndexOf(name));
      if (duplicatePart) {
        // 如果选择了重复的配件，可以在这里进行处理，比如清空选择或给出提示
        alert("不允许有重复的配件名!")
        console.log(duplicatePart)
        this.sale_order.parts = oldVal
        return;
      }
      this.sale_order.total_price = 0;
      for (let i = 0; i < this.sale_order.parts.length; i++) {
        const row = this.sale_order.parts[i];
        row.total_price = row.quantity * row.average_price;
        if ( isNaN(row.total_price) ) {
          this.sale_order.total_price = null;
        } else {
          this.sale_order.total_price += row.total_price;
        }
      }
    },
    handleSwitchChange() {
      if (this.sale_order.status === 0) {
        this.pay_method = null;
        this.payee = null;
      }
    },
    async getEmployees() {
      try {
        const response = await GetEmployees();
        return response.data.data;
      } catch (error) {
        console.error('Error fetching employees:', error);
        return []; // 返回空数组或者其他默认值
      }
    },
    async getVehicles() {
      try {
        const response = await GetVehicles();
        return response.data.data;
      } catch (error) {
        console.error('Error fetching vehicles:', error);
        return []; // 返回空数组或者其他默认值
      }
    },
    async getVehicleParts() {
      try {
        const response = await GetVehicleParts();
        return response.data.data
      } catch (error) {
        console.error('Error fetching vehicle parts:', error);
        return []; // 返回空数组或者其他默认值
      }
    },
    handlePartSelectClick() {
      // console.log(this.parts);
    },
    removePart(part) {
      var index = this.sale_order.parts.indexOf(part);
      if (index !== -1) {
        if (this.sale_order.parts[index].id) {
          DelOrderPart(this.sale_order.parts[index].id);
        }
        this.sale_order.parts.splice(index, 1);
      }
    },
      // 新增表单
    addPart() {
      this.sale_order.parts.push(
        {
          id: null,
          vehicle_part: {
            id: '',
            name: '',
            estimated_price: 0,
          },
          average_price: null,
          quantity: 1,
          total_price: 0,
        }
      );
    },
    async handleButtonSave() {
      const employee_ids = this.sale_order.employees.map(emp => emp.id);
      let sale_order = {
        "total_price": this.sale_order.total_price,
        "real_price": this.sale_order.real_price ? this.sale_order.real_price : 0,
        "discounted_price": 0,
        "datetime": this.sale_order.datetime,
        "vehicle": this.sale_order.vehicle.id,
        "employees": employee_ids,
        "current_mile": this.sale_order.current_mile,
        "status": this.sale_order.status,
      }
      if (this.sale_order.status === 1) {
        sale_order.payee = this.sale_order.payee.id;
        sale_order.pay_method = this.sale_order.pay_method.id;
      }
      console.log(sale_order)
      try {
        var response;
        sale_order.id = this.sale_order.id;
        response = await UpdateSaleOrder(sale_order);
        console.log("response: ")
        console.log(response)
        for (var i = 0; i < this.sale_order.parts.length; i++) {
          let order_part = {
            "id": this.sale_order.parts[i].id,
            "vehicle_part": this.sale_order.parts[i].vehicle_part.id,
            "sale_order": this.sale_order.id,
            "quantity": this.sale_order.parts[i].quantity,
            "average_price": this.sale_order.parts[i].average_price,
            "total_price": this.sale_order.parts[i].total_price
          } 
          if (order_part.id) {
            console.log(order_part)
            await UpdateOrderPart(order_part);
            console.log("更新消费单配件")
          } else {
            var response
            response = await AddOrderPart(order_part);
            console.log("新增消费单配件")
            console.log(response)
            this.sale_order.parts[i].id = response.data.id;
          }
        }
        this.$message({
          message: '保存消费单成功',
          type: 'success'
        });
        this.closeThis();
      } catch (error) {
        this.$message.error('保存消费单失败');
        console.error('Error adding sale_order:', error);
      }
    },
  }
}
</script>

<style lang="scss">
.container {
  display: flex;
  justify-content: center;
}
</style>