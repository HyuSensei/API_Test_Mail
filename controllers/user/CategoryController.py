from fastapi import HTTPException, status
from database import SessionLocal
import models

def handleCategory(id,page,limit):
    db=SessionLocal()
    get_category_skincare= db.query(models.Category).filter(models.Category.category_parent_id==1).all()
    get_category_makeup= db.query(models.Category).filter(models.Category.category_parent_id==2).all()
    limit = 8
    start = (page - 1) * limit
    get_product= db.query(models.Product).filter(models.Product.category_id==id)
    total = get_product.count()
    products = get_product.offset(start).limit(limit).all()
    total_page = (total // limit) + (1 if total % limit > 0 else 0)
    current_page = page if page <= total_page else total_page
    return {
        "success":True,
        "category_id":id,
        "category_skincare":get_category_skincare,
        "category_makeup":get_category_makeup,
        "products":products,
        "total_page":total_page,
        "current_page":current_page
    }