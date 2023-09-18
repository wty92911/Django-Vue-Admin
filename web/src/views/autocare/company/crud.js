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
        title: 'ID',
        key: 'id',
        disabled: true,
        form: {
          disabled: true
        }
      },
      {
        title: '供货商',
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
              message: '供货商为必填项'
            }
          ],
          component: {
            span: 12,
            placeholder: '请输入供货商'
          },
          itemProps: {
            class: { yxtInput: true }
          }
        }
      },
      {
        title: '联系电话',
        key: 'mobile',
        search: {
          disabled: false
        },
        minWidth: 110,
        type: 'input',
        form: {
          rules: [
            {
              max: 20,
              message: '请输入正确的联系电话',
              trigger: 'blur'
            },
            {
              pattern: /^(?:(?:\+?86)?1[3456789]\d{9})|(?:\d{3,4}-\d{7,8}(?:-\d{1,4})?)$/,
              message: '请输入正确的联系电话'
            }
          ],
          itemProps: {
            class: { yxtInput: true }
          },
          component: {
            placeholder: '请输入联系电话'
          }
        }
      },
      {
        title: '采购总金额(元)',
        key: 'total_real_price',
        minWidth: 90,
        search: {
          disabled: true
        },
        form: {
          disabled: true,
          component: {
            placeholder: ''
          }
        },

      }

    ].concat(vm.commonEndColumns({
      create_datetime: { showTable: false },
      update_datetime: { showTable: false }
    }))
  }
}
