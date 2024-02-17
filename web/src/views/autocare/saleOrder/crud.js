import { request } from '@/api/service'
import {urlPrefix as vehiclePrefix} from '@/views/autocare/vehicle/api'
export const crudOptions = (vm) => {
  // util.filterParams(vm, ['dept_name', 'role_info{name}', 'dept_name_all'])
  return {
    pageOptions: {
      compact: true
    },
    options: {
      height: '100%',
      // tableType: 'vxe-table',
      // rowKey: true,
      rowId: 'id'
    },
    selectionRow: {
      align: 'center',
      width: 46
    },
    rowHandle: {
      width: 240,
      fixed: 'right',
      view: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Retrieve')
        },
        show: false,
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        },
        show: false,
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        },
        
      },
      custom: [
        {
          thin: true,
          span: 12,
          text: '',
          type: 'primary',
          icon: 'el-icon-edit',
          size: 'small',
          emit: 'customEdit'  //自定义按钮事件
        }
      ]
    },
    viewOptions: {
      componentType: 'form'
    },
    formOptions: {
      defaultSpan: 12 // 默认的表单 span
    },
    indexRow: { // 或者直接传true,不显示title，不居中
      title: '序号',
      align: 'center',
      width: 60
    },
    columns: [
      {
        title: '关键词',
        key: 'search',
        show: false,
        disabled: true,
        search: {
          disabled: true,
        },
        form: {
          disabled: true,
          component: {
            placeholder: '请输入关键词'
          }
        },
        view: {
          disabled: true
        }
      },
      {
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '消费车辆',
        key: 'vehicle',
        sortable: 'custom',
        minWidth: 90,
        search: {
          disabled: false
        },
        formatter: (row, col, cellValue, index) => {
          return row.plate_number
        },
        type: 'select',
        dict: {
          url: vehiclePrefix,
          value: 'id', // 数据字典中value字段的属性名
          label: 'plate_number', // 数据字典中label字段的属性名
          cache: false,
          getData: (url, dict, { form, component }) => { // 配置此参数会覆盖全局的getRemoteDictFunc
            return request({url: url}).then(ret=>{
              // console.log(ret.data)
              return ret.data.data
            })
          }
        },
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '消费车辆必填'
            },
          ],
          component: {
            span: 12,
            placeholder: '请输入或选择消费车辆',
            filterable: true,
            clearable: true,
            on: {
              change: (event) => {
                // console.log(event)
              }
            }
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '里程数(公里)',
        key: 'current_mile',
        show: true,
        search: {
          disabled: true,
        },
        type: 'input',
        form: {
          rules: [
            {
              required: false,
              message: ''
            },
            {
              
              pattern: /^(0|[1-9]\d*)$/,
              message: '请输入整数'
            }
          ],
          component: {
            span: 12,
          }
        }
      },
      {
        title: '消费总价(元)',
        key: 'total_price',
        show: true,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          rules: [
            {
              required: false,
              message: ''
            },
            {
              pattern: /^(0|[1-9]\d*)$/,
              message: '请输入整数'
            }
          ],
          component: {
          }
        }
      },
      {
        title: '实际支付(元)',
        key: 'real_price',
        show: true,
        search: {
          disabled: true
        },
        type: 'input',
      },
      {
        title: '状态',
        key: 'status',
        show: true,
        search: {
          disabled: false,
        },
        type: 'select',
        dict: {
          data: vm.dictionary('sale_order_status')
        },
        form: {
          rules: [
            {
              required: false,
              message: ''
            },
          ],
          component: {
          }
        }
      },
    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
  }
}
