from fastapi import APIRouter, HTTPException, status
from controllers.user import OrderController
import models
from pydantic import BaseModel

router=APIRouter()

class CartBase(BaseModel):
    id: int
    price: float
    quantity: int
    class Config:
        arbitrary_types_allowed = True
    
class UserBase(BaseModel):
    name: str
    address: str
    phone: str
    user_id: int
    method: str
    class Config:
        arbitrary_types_allowed = True

class OrderBase(BaseModel):
    cart: list[CartBase]
    user: UserBase
    class Config:
        arbitrary_types_allowed = True

@router.post("/api/v1/order",status_code=status.HTTP_201_CREATED)
def handleOrder(order: OrderBase):
    try:
        data_order = order.dict()
        get_data = OrderController.addOrder(data_order)
        print(get_data)
        return get_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
        
@router.get("/api/v1/orderConfirm/{user_id}",status_code=status.HTTP_200_OK)
def getOrderConfirm(user_id:int):
    try:
        data_order= OrderController.handleOrderConfirm(user_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/orderShip/{user_id}",status_code=status.HTTP_200_OK)
def getOrderShip(user_id:int):
    try:
        data_order= OrderController.handleOrderShip(user_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/orderComplete/{user_id}",status_code=status.HTTP_200_OK)
def getOrderShip(user_id:int):
    try:
        data_order= OrderController.handleOrderComplete(user_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/orderCancel/{user_id}",status_code=status.HTTP_200_OK)
def getOrderCancel(user_id:int):
    try:
        data_order= OrderController.handleOrderCancel(user_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/updateStatusOrder/{order_id}",status_code=status.HTTP_200_OK)
def getUpdateStatus(order_id:int):
    try:
        data_order= OrderController.handleUpdateStatus(order_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/actionCancelOrder/{order_id}",status_code=status.HTTP_200_OK)
def cancelOrder(order_id:int):
    try:
        data_order= OrderController.handleCancelOrder(order_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/orderRate/{user_id}/{order_id}")
def getUpdateOrder(user_id:int,order_id:int):
    try:
        data_order= OrderController.handleOrderRate(user_id,order_id)
        return data_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

