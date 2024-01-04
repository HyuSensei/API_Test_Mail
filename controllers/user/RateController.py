from fastapi import HTTPException, status
from database import SessionLocal
import models 

def handleRate(rate):
    db=SessionLocal()
    db.add(rate)
    db.commit()
    db.refresh(rate)
    return {
        "success": True,
        "message": "Đánh giá sản phẩm thành công !",
        "rate": rate
    }

