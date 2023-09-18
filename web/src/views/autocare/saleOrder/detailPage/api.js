import { GetList as getVehicles } from '@/views/autocare/vehicle/api'
import { GetList as getVehicleParts} from '@/views/autocare/vehiclePart/api'
import { GetList as getEmployees} from '@/views/autocare/employee/api'
export function GetVehicles(query) {
    return getVehicles(query)
}

export function GetVehicleParts(query) {
    return getVehicleParts(query)
}
export function GetEmployees(query) {
    return getEmployees(query)
}

const urlSaleOrderParts = '/api/autocare/sale_vehicle_part/'
export function AddObjParts(query) {
    return request({
        url: urlSaleOrderParts,
        method: 'post',
        data: obj
      })
}

export function UpdateObj (obj) {
    return request({
      url: urlSaleOrderParts + obj.id + '/',
      method: 'put',
      data: obj
    })
  }
