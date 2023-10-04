import { GetList as getVehicles } from '@/views/autocare/vehicle/api'
import { GetList as getVehicleParts} from '@/views/autocare/vehiclePart/api'
import { GetList as getEmployees} from '@/views/autocare/employee/api'
import { GetList as getOrderPart, DelObj as delOrderPart, UpdateObj as updateOrderPart, AddObj as addOrderPart} from '@/views/autocare/saleOrderPart/api'
export function GetVehicles(query) {
    return getVehicles(query)
}
export function GetVehicleParts(query) {
    return getVehicleParts(query)
}
export function GetEmployees(query) {
    return getEmployees(query)
}
export function GetOrderPart(query) {
    return getOrderPart(query);
}
export function DelOrderPart(query) {
    return delOrderPart(query);
}
export function UpdateOrderPart(query) {
    return updateOrderPart(query);
}
export function AddOrderPart(query) {
    return addOrderPart(query);
}