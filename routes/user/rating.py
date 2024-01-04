from fastapi import APIRouter, HTTPException, status
from controllers.user import RateController
import models
from pydantic import BaseModel

router=APIRouter()

class RateBase(BaseModel):
    product_id: int
    user_id : int
    order_id : int
    star: int
    comment: str
    class Config:
        arbitrary_types_allowed = True

@router.post("/api/v1/rate",status_code=status.HTTP_201_CREATED)
def handleRateOrder(rate: RateBase):
    try:
        data_order = models.Rate(**rate.dict())
        get_data = RateController.handleRate(data_order)
        print(get_data)
        return get_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    
    