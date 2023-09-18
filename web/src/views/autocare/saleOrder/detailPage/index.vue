<template>
	<d2-container :class="{ 'page-compact': true }">
		<el-main>
		<el-form>
			<el-form-item>
			<el-date-picker
				v-model="sale_order.datetime"
				type="datetime"
				style="width: 20%; font-weight: bold; margin-right: 5px"
				placeholder="选择日期时间">
    	</el-date-picker>
			派工<el-select 
				v-model="sale_order.employees"
				value-key="name" 
				filterable multiple
				style="width: 20%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
				placeholder="请派工" >
				<el-option
					v-for="item in all_employees"
					:key="item.id"
					:label="item.name"
					:value="item">
				</el-option>
			</el-select>
			总价<el-input
				v-model="sale_order.total_price"
				style="width: 10%; margin-left: 10px; font-weight: bold; margin-right: 10px;"
				placeholder="消费单总价"
				prefix-icon="el-icon-coin"
				readonly
			></el-input>
      <el-button
        v-if="type === 'edit'"
        @click="handleButtonSettle"
        type="warning"
        style="margin-top: 10px; width: 10%; margin-left: 10px;"
      >结算消费单</el-button>
      <el-dialog title="结算" :visible.sync="dialogSettleVisible">
        <el-form>
          <el-form-item>
            <i class="el-icon-s-shop"></i><el-select 
              v-model="sale_order.pay_method"
              value-key="name" 
              filterable
              style="width: 30%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
              placeholder="请选择支付方式" >
              <el-option
                v-for="item in all_pay_methods"
                :key="item.id"
                :label="item.name"
                :value="item">
              </el-option>
            </el-select>
            <br>
            <i class="el-icon-user"></i><el-select 
              v-model="sale_order.payee"
              value-key="name" 
              filterable
              style="width: 30%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
              placeholder="请选择收款人" >
              <el-option
                v-for="item in all_employees"
                :key="item.id"
                :label="item.name"
                :value="item">
              </el-option>
            </el-select>
            <br>
            <i class="el-icon-coin"></i><el-input 
              v-model="sale_order.real_price"
              style="width: 30%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
              placeholder="请输入收款金额" >
            </el-input>
          </el-form-item>
        </el-form>
        <div 
          slot="footer" class="dialog-footer"
          style="display: flex; justify-content: space-between;">
          <el-button @click="dialogSettleVisible = false">取 消</el-button>
          <el-button type="primary" @click="handleCommitSettle">确 定</el-button>
        </div>
      </el-dialog>
		</el-form-item>
	<el-form-item>
			<el-select 
				v-model="sale_order.vehicle"
				value-key="plate_number" 
				style="width: 20%"
				filterable placeholder="请输入或选择车牌号" >
				<el-option
					v-for="item in all_vehicles"
					:key="item.id"
					:label="item.plate_number"
					:value="item">
				</el-option>
			</el-select>
			<el-input
				v-model="sale_order.vehicle.customer_name"
				style="width: 20%; margin-left: 10px"
				placeholder="车主姓名"
				prefix-icon="el-icon-s-custom"
				disabled
			></el-input>
			<el-input
				v-model="sale_order.vehicle.customer_mobile"
				style="width: 20%; margin-left: 10px; margin-right: 5px"
				placeholder="车主电话"
				prefix-icon="el-icon-mobile-phone"
				disabled
			></el-input>
			里程<el-input 
				v-model="sale_order.current_mile"
				style="width: 10%; margin-left: 10px"
				placeholder="当前里程数" >
			<i slot="suffix" style="font-style: normal; margin-right: 10px">KM</i>
			</el-input>
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
							v-model="scope.row.part"
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
							v-model="scope.row.part.estimated_price"
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
import { GetVehicles, GetVehicleParts, GetEmployees} from './api'
import { AddObj as AddSaleOrder, UpdateObj as UpdateSaleOrder} from '../api'
import { mapState, mapActions } from 'vuex'
export default {
  name: 'saleOrderDetailPage',
  data () {
    return {
				type: 'add',
        dialogSettleVisible: false,
        // vehicle: {
        //     plate_number: '',
        //     customer: {
        //         name: '',
        //         mobile: '',
        //     }
        // },
				sale_order: {
					id: null,
					current_mile: '',
					datetime: new Date(),
					discounted_price: null,
					employees: null,
					parts: [
							{
									part: {
										id: '',
										name: '',
										estimated_price: 0,
									},
									quantity: 1,
									average_price: '',
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
			all_employees: null,
			all_vehicle_parts: null,
			all_vehicles: null,

    };
  },
  created() {
		// this.getVehicles().then(data => {
		// 	this.all_vehicles = data;
    // });
    // this.getVehicleParts().then(data => {
		// 	this.all_vehicle_parts = data;
		// 	// console.log(this.vehicle_parts)
    // });
		// this.getEmployees().then(data => {
		// 	this.all_employees = data;
		// });
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

      // 继续执行 loadSaleOrderData 方法
      if (this.$route.params.sale_order) {
        this.loadSaleOrderData();
      }
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
	},
  computed: {
		
    handleNaN() {
			return (num) => isNaN(num) ? "请先输入实际单价" : num;
    },
    totalPrice() {
			return (row) => row.quantity & row.part.average_price ? row.quantity * row.part.average_price : '';
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
    handleCommitSettle() {
      this.dialogSettleVisible = false;
      this.sale_order.payee = this.sale_order.payee.id;
      this.sale_order.pay_method = this.sale_order.pay_method.id;
      this.sale_order.status = 1;
      this.handleButtonSave();
    },
    handleButtonSettle() {
      this.dialogSettleVisible = true;
    },
    selectPaymentMethod(paymentAmount) {
      this.sale_order.real_price = paymentAmount
      // 在这里处理选择支付方式和支付金额的逻辑
      // 可以打开另一个对话框或弹出框来选择支付方式
      // 并将支付金额作为参数传递给相应的处理方法
    },
    loadSaleOrderData() {
      this.type = 'edit';
      this.sale_order = { ...this.$route.params.sale_order };
      this.sale_order.vehicle = this.all_vehicles.find(vehicle => vehicle.id === this.sale_order.vehicle);
      this.sale_order.datetime = new Date(this.sale_order.datetime);
      this.sale_order.parts = JSON.parse(this.sale_order.parts);
      console.log(this.sale_order);
    },
    updateTotalPrice(newVal, oldVal) {
			const selectedParts = this.sale_order.parts.map(item => item.part.name);
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
				// if ( row.quantity & row.part.average_price ) {
				row.total_price = row.quantity * row.average_price;
				if ( isNaN(row.total_price) ) {
					this.sale_order.total_price = null;
				} else {
					this.sale_order.total_price += row.total_price;
				}
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
					this.sale_order.parts.splice(index, 1);
			}
    },
    	// 新增表单
    addPart() {
			this.sale_order.parts.push(
				{
					part: {
						id: '',
						name: '',
						estimated_price: 0,
					},
					average_price: '',
					quantity: 1,
					total_price: 0,
				}
			);
    },
   	async handleButtonSave() {
			const employee_ids = this.sale_order.employees.map(emp => emp.id);
			let parts_json = JSON.stringify(this.sale_order.parts);
			let sale_order = {
				"total_price": this.sale_order.total_price,
				"real_price": 0,
				"discounted_price": 0,
				"datetime": this.sale_order.datetime,
				"vehicle": this.sale_order.vehicle.id,
				"employees": employee_ids,
				"current_mile": this.sale_order.current_mile,
				"status": this.sale_order.status,
				"parts": parts_json,
        "payee": this.sale_order.payee,
        "pay_method": this.sale_order.pay_method,
			}
			console.log(sale_order)
			try {
        var response;
        if (this.type === 'edit') {
          sale_order.id = this.sale_order.id;
          response = await UpdateSaleOrder(sale_order);
        } else {
          response = await AddSaleOrder(sale_order);
        }
        console.log("response: ")
        console.log(response)
        // return response.data.data
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
</style>