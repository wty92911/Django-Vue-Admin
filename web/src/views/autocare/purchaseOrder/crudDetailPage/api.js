import { GetList as getEmployees} from '@/views/autocare/employee/api'
import { GetList as getVehicleParts} from '@/views/autocare/vehiclePart/api'
import { GetList as getCompanys} from '@/views/autocare/company/api'
import { GetList as getOrderPart, DelObj as delOrderPart, UpdateObj as updateOrderPart, AddObj as addOrderPart} from '@/views/autocare/purchaseOrderPart/api'
export function GetEmployees(query) {
	return getEmployees(query);
}
export function GetVehicleParts(query) {
	return getVehicleParts(query);
}
export function GetCompanys(query) {
	return getCompanys(query);
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