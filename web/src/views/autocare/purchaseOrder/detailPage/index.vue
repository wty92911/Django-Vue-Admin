<template>
	<d2-container :class="{ 'page-compact': true }">
		<el-main>
		<el-form>
			<el-form-item>
			<el-date-picker
				v-model="purchase_order.datetime"
				type="datetime"
				style="width: 20%; font-weight: bold; margin-right: 5px"
				placeholder="选择日期时间">
    	</el-date-picker>
			供应商<el-select 
				v-model="purchase_order.supply_company"
        value-key="name"
				style="width: 20%; margin-left: 10px; margin-right: 10px;"
				filterable placeholder="请输入或选择供应商"
        >
        <template slot="prefix">
          <span style="padding-left: 5px;">
            <i class="el-icon-office-building"></i>
          </span>
        </template>
				<el-option
					v-for="item in all_supply_companys"
					:key="item.id"
					:label="item.name"
					:value="item">
				</el-option>
			</el-select>
			总价<el-input
				v-model="purchase_order.total_price"
				style="width: 10%; margin-left: 10px; font-weight: bold; margin-right: 10px;"
				placeholder="采购单总价"
				prefix-icon="el-icon-coin"
				readonly
			></el-input>
		</el-form-item>
    <el-form-item>
    <el-select 
      v-model="purchase_order.pay_method"
      value-key="name" 
      filterable
      style="width: 20%; margin-right: 5px; font-weight: bold;"
      placeholder="请选择支付方式" >
      <template slot="prefix">
        <span style="padding-left: 5px;">
          <i class="el-icon-s-shop"></i>
        </span>
      </template>
      <el-option
        v-for="item in all_pay_methods"
        :key="item.id"
        :label="item.name"
        :value="item">
      </el-option>
    </el-select>
    付款人<el-select 
      v-model="purchase_order.payer"
      value-key="name" 
      filterable
      style="width: 20%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
      placeholder="请选择付款人" >
      <template slot="prefix">
        <span style="padding-left: 5px;">
          <i class="el-icon-user"></i>
        </span>
      </template>
      <el-option
        v-for="item in all_employees"
        :key="item.id"
        :label="item.name"
        :value="item">
      </el-option>
    </el-select>
    实际支付<el-input 
      v-model="purchase_order.real_price"
      style="width: 15%; margin-left: 10px; margin-right: 5px; font-weight: bold;"
      prefix-icon="el-icon-coin"
      placeholder="请输入付款金额" >
    </el-input>
  </el-form-item>
			<el-table  :data="purchase_order.parts" style="margin-top: 20px; width: 100%">
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
				<el-table-column label="历史进价(元)" min-width="10%">
					<template slot-scope="scope">
						<!-- <el-input
							v-model="scope.row.part.estimated_price"
							placeholder=""
							disabled
						></el-input> -->
            <el-button @click="showHistoryPriceChart(scope.row.vehicle_part)"
              :disabled="(scope.row.vehicle_part && scope.row.vehicle_part.id) ? false : true"
            ><i class="el-icon-time"></i></el-button>
            
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
							{{ handleNaN(scope.row.total_price) }}
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
					>新增采购配件</el-button>
					<el-button
						@click="handleButtonSave"
						type="success"
						style="margin-top: 10px; width: 10%;"
					>保存采购单</el-button>
			  </div>
			</el-form-item>
		</el-form>
		</el-main>
    <el-dialog title="历史单价" :visible.sync="historyPriceChartVisiable">
      <!-- X: 时间、供货商、Y: 均价 -->
      <div class="chart">
        <line-chart :data="history_price_chart_data" />
      </div>
    </el-dialog>
	</d2-container>
</template>
<script>
import { GetCompanys, GetVehicleParts, GetEmployees, GetOrderPart, DelOrderPart, UpdateOrderPart, AddOrderPart} from './api'
import { AddObj as AddSaleOrder, UpdateObj as UpdateSaleOrder} from '../api'
import { mapState, mapActions } from 'vuex'
export default {
  name: 'purchaseOrderDetailPage',
  components: {
  },
  data () {
    return {
		    type: 'add',
        historyPriceChartVisiable: false,
        // vehicle: {
        //     plate_number: '',
        //     customer: {
        //         name: '',
        //         mobile: '',
        //     }
        // },
				purchase_order: {

					id: null,
					datetime: new Date(),
          supply_company: null,
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
          payer: null,
          pay_method: null,
					real_price: null,
					total_price: null,
			},
      all_employees: null,
			all_vehicle_parts: null,
			all_supply_companys: null,
      history_price_chart_data: null,

    };
  },
  created() {
    // 使用 Promise.all 等待多个异步操作完成
    Promise.all([
      this.getVehicleParts(),
      this.getEmployees(),
      this.getCompanys(),
    ]).then(([vehiclePartsData, employeesData, companysData]) => {
      // 将获取的数据分别赋值给相应的属性
      this.all_vehicle_parts = vehiclePartsData;
      this.all_employees = employeesData;
      this.all_supply_companys = companysData;
      // 继续执行 loadPurchaseOrderData 方法
      if (this.$route.params.purchase_order) {
        this.loadPurchaseOrderData();
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
    ];
  },
	mounted() {
	},
  computed: {
		
    handleNaN() {
			return (num) => isNaN(num) ? "请先输入实际单价" : num;
    },
    // isHistoryPriceChartDisabled() {
    //   return (part && part.id) ? false : true;
    // },
  },
  watch: {
    'purchase_order.parts': {
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
    loadPurchaseOrderData() {
      this.type = 'edit';
      this.purchase_order = { ...this.$route.params.purchase_order };
      this.purchase_order.datetime = new Date(this.purchase_order.datetime);
      this.purchase_order.supply_company = this.all_supply_companys.find(company => company.id === this.purchase_order.supply_company);
      this.purchase_order.payer = this.all_employees.find(emp => emp.id === this.purchase_order.payer);
      this.purchase_order.pay_method = this.all_pay_methods.find(method => method.id === this.purchase_order.pay_method);
      console.log(this.purchase_order);
    },
    updateTotalPrice(newVal, oldVal) {
			const selectedParts = this.purchase_order.parts.map(item => item.vehicle_part.name);
			const duplicatePart = selectedParts.find(name => selectedParts.indexOf(name) !== selectedParts.lastIndexOf(name));
			if (duplicatePart) {
				// 如果选择了重复的配件，可以在这里进行处理，比如清空选择或给出提示
				alert("不允许有重复的配件名!")
				console.log(duplicatePart)
				this.purchase_order.parts = oldVal
				return;
			}
			this.purchase_order.total_price = 0;
			for (let i = 0; i < this.purchase_order.parts.length; i++) {
				const row = this.purchase_order.parts[i];
				// if ( row.quantity & row.part.average_price ) {
				row.total_price = row.quantity * row.average_price;
				if ( isNaN(row.total_price) ) {
					this.purchase_order.total_price = null;
				} else {
					this.purchase_order.total_price += row.total_price;
				}
			}
    },
    async getCompanys() {
			try {
				const response = await GetCompanys();
				return response.data.data;
			} catch (error) {
				console.error('Error fetching companys:', error);
				return []; // 返回空数组或者其他默认值
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
    
    async showHistoryPriceChart(part) {
      this.history_price_chart_data = [];
      const response = await GetOrderPart({"vehicle_part": part.id});
      console.log("showHistoryPriceChart");
      console.log(response);
      
      const history_price_parts = response.data.data;
      this.history_price_chart_data = [
        {
          name: part.name + "历史单价",
          data: history_price_parts.map(part => ({label: part.create_datetime, value: part.average_price})).sort((a, b) => new Date(a.label) - new Date(b.label))
        }
      ]
      
      console.log(this.history_price_chart_data)
      if (response.data.data.length < 1) {
        this.$message.error('查询配件历史价格失败: 数据不足');
        return;
      }
      this.historyPriceChartVisiable = true;
    },
    removePart(part) {
			var index = this.purchase_order.parts.indexOf(part);
			if (index !== -1) {
        if (this.purchase_order.parts[index].id) {
          DelOrderPart(this.purchase_order.parts[index].id);
        }
				this.purchase_order.parts.splice(index, 1);
			}
    },
    	// 新增表单
    addPart() {
			this.purchase_order.parts.push(
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
      
			let purchase_order = {
				"total_price": this.purchase_order.total_price,
				"real_price": this.purchase_order.real_price ? this.purchase_order.real_price: this.purchase_order.total_price,
				"datetime": this.$moment(this.purchase_order.datetime).format('YYYY-MM-DD hh:mm:ss'),
        "payer": this.purchase_order.payer.id,
        "pay_method": this.purchase_order.pay_method.id,
        "supply_company": this.purchase_order.supply_company.id,
			}
			console.log(purchase_order)
			try {
        var response;
        if (this.type === 'edit') {
          purchase_order.id = this.purchase_order.id;
          response = await UpdateSaleOrder(purchase_order);
        } else {
          response = await AddSaleOrder(purchase_order);
          this.purchase_order.id = response.data.id;
        }
        console.log("response: ")
        console.log(response)
        // return response.data.data
        for (var i = 0; i < this.purchase_order.parts.length; i++) {
          let order_part = {
            "id": this.purchase_order.parts[i].id,
            "vehicle_part": this.purchase_order.parts[i].vehicle_part.id,
            "purchase_order": this.purchase_order.id,
            "quantity": this.purchase_order.parts[i].quantity,
            "average_price": this.purchase_order.parts[i].average_price,
            "total_price": this.purchase_order.parts[i].total_price
          }
          
          if (order_part.id) {
            console.log(order_part)
            await UpdateOrderPart(order_part);
          } else {
            var response
            response = await AddOrderPart(order_part);
            console.log("新增采购单配件")
            console.log(response)
            this.purchase_order.parts[i].id = response.data.id;
          }
        }
        this.$message({
          message: '保存采购单成功',
          type: 'success'
        });
        this.closeThis();
			} catch (error) {
				this.$message.error('保存采购单失败');
				console.error('Error adding purchase_order:', error);
			}
    },
  }
}
</script>

<style scoped lang="scss">
.chart {
  width: 100%;
  height: 300px;
}
</style>