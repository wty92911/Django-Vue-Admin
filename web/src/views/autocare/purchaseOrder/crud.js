import { request } from '@/api/service'
import {urlPrefix as companyPrefix} from '@/views/autocare/company/api'
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
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '供货商',
        key: 'supply_company',
        sortable: 'custom',
        minWidth: 90,
        search: {
          disabled: false,
        },
        type: 'select',
        dict: {
          url: companyPrefix,
          value: 'id', // 数据字典中value字段的属性名
          label: 'name', // 数据字典中label字段的属性名
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
              message: '供应商必填'
            },
          ],
          component: {
            span: 12,
            placeholder: '请输入或选择供应商',
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
        title: '进货日期',
        key: 'datetime',
        sortable: 'custom',
        minWidth: 150,
        search: {
          disabled: false,
        },
        type: 'datetime',
        
      },
      {
        title: '采购单总额',
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
        title: '实付款',
        key: 'real_price',
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
        title: '配件列表',
        key: 'parts',
        form: {
          slot: true,
        },
        rowSlot: true,
      },
    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
  }
}
