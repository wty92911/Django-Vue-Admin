import { request } from '@/api/service'
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
        }
      },
      edit: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Update')
        }
      },
      remove: {
        thin: true,
        text: '',
        disabled () {
          return !vm.hasPermissions('Delete')
        }
      },
      custom: []
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
        title: '配件名',
        key: 'name',
        sortable: 'custom',
        minWidth: 90,
        search: {
          disabled: false
        },
        type: 'input',
        form: {
          rules: [ // 表单校验规则
            {
              required: true,
              message: '配件名必填'
            },
          ],
          component: {
            span: 12,
            placeholder: '请输配件名'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '库存量',
        key: 'inventory_quantity',
        show: true,
        search: {
          disabled: false,
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
            placeholder: '查询小于等于库存量'
          }
        }
      },
      {
        title: '库存总额(元)',
        key: 'inventory_total_price',
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
        title: '库存均价(元)',
        key: 'inventory_average_price',
        show: true,
        search: {
          disabled: true
        },
        type: 'status',
        form: {
          component: {
          }
        }
      },
      {
        title: '预估单价(元)',
        key: 'estimated_price',
        show: true,
        search: {
          disabled: true
        },
        type: 'input',
        form: {
          component: {
          }
        }
      }
    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
  }
}
