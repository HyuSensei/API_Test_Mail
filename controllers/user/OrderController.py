from fastapi import HTTPException, status
from database import SessionLocal
import models 
from sqlalchemy import func, distinct

def addOrder(data_order):
    db= SessionLocal()
    data_cart= data_order["cart"]
    if len(data_cart)==0:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="Vui lòng thêm sản phẩm vào giỏ hàng !"
        )
    data_user= data_order["user"]
    if (not data_user["name"]) or (not data_user["address"]) or (not data_user["phone"]) or (not data_user["user_id"]):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="Vui lòng điền đầy đủ thông tin đặt hàng !"
        )
    if (not data_user["method"]):
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="Vui lòng chọn phương thức thanh toán !"
        )
    if data_user["method"]=="ordervnpay":
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST, detail="Hiện tại website SkinLeLe chưa hỗ trợ thanh toán VNPAY !"
        )
    total=0
    for i in range(len(data_cart)):
        total = data_cart[i]["price"] * data_cart[i]["quantity"]
    order_info = models.Order(
    payment="Thanh toán khi nhận hàng!",
    status=0,
    name=data_user["name"],
    address=data_user["address"],
    phone=data_user["phone"],
    total=total,
    user_id=data_user["user_id"]
    )
    db.add(order_info)
    db.commit()
    max_id_order = db.query(func.max(models.Order.id)).scalar()
    for i in range(len(data_cart)):
       order_product= models.OrderProduct(
           order_id= max_id_order,
           product_id= data_cart[i]["id"],
           quantity= data_cart[i]["quantity"]
       )
       db.add(order_product)
       db.commit()
    return {
        "success": True,
        "message": "Đặt hàng thành công !",
    }

def handleOrderConfirm(user):
    db=SessionLocal()
    query = (
    db.query(models.Order, models.Product,models.OrderProduct)
    .join(models.OrderProduct, models.Order.id == models.OrderProduct.order_id)
    .join(models.Product, models.OrderProduct.product_id == models.Product.id)
    .filter(models.Order.user_id == user)
    .filter(models.Order.status == 0)
    )
    results = query.all()
    data_order=[]
    last_product=[]
    max_order=[]
    get_last_product=[]
    for order, product, order_product in results:
        get_order={
            "id":order.id,
            "payment": order.payment,
            "status": order.status,
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "user_id": order.user_id,
            "total": order.total,
            "product_id": order_product.product_id,
            "quantity": order_product.quantity,
            "product_price": product.price,
            "product_name": product.name,
            "product_image": product.image 
        }
        check_last_order = db.query(func.max(models.OrderProduct.id)).filter(models.OrderProduct.order_id == order.id).scalar()
        if check_last_order not in max_order:
            max_order.append(check_last_order)
        data_order.append(get_order)
    for i in max_order:
        check_last_product= db.query(models.OrderProduct.product_id).filter(models.OrderProduct.id == i).first()
        last_product.append(check_last_product)
    get_last_product = [result[0] for result in last_product]
    return {
        "success":True,
        "message":"Thông tin đơn hàng đang chờ xác nhận !",
        "order": data_order,
        "last_product": get_last_product
    }
    
def handleOrderShip(user):
    db=SessionLocal()
    query = (
    db.query(models.Order, models.Product,models.OrderProduct)
    .join(models.OrderProduct, models.Order.id == models.OrderProduct.order_id)
    .join(models.Product, models.OrderProduct.product_id == models.Product.id)
    .filter(models.Order.user_id == user)
    .filter(models.Order.status == 1)
    )
    results = query.all()
    data_order=[]
    last_product=[]
    max_order=[]
    get_last_product=[]
    for order, product, order_product in results:
        get_order={
            "id":order.id,
            "payment": order.payment,
            "status": order.status,
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "user_id": order.user_id,
            "total": order.total,
            "product_id": order_product.product_id,
            "quantity": order_product.quantity,
            "product_price": product.price,
            "product_name": product.name,
            "product_image": product.image  
        }
        check_last_order = db.query(func.max(models.OrderProduct.id)).filter(models.OrderProduct.order_id == order.id).scalar()
        if check_last_order not in max_order:
            max_order.append(check_last_order)
        data_order.append(get_order)
    for i in max_order:
        check_last_product= db.query(models.OrderProduct.product_id).filter(models.OrderProduct.id == i).first()
        last_product.append(check_last_product)
    get_last_product = [result[0] for result in last_product]
    return {
        "success":True,
        "message":"Thông tin đơn hàng đang vận chuyển !",
        "order": data_order,
        "last_product": get_last_product
    }

def handleOrderComplete(user):
    db=SessionLocal()
    query = (
    db.query(models.Order, models.Product,models.OrderProduct)
    .join(models.OrderProduct, models.Order.id == models.OrderProduct.order_id)
    .join(models.Product, models.OrderProduct.product_id == models.Product.id)
    .filter(models.Order.user_id == user)
    .filter(models.Order.status == 2)
    )
    results = query.all()
    data_order=[]
    last_product=[]
    max_order=[]
    get_last_product=[]
    count_check=[]
    for order, product, order_product in results:
        get_order={
            "id":order.id,
            "payment": order.payment,
            "status": order.status,
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "user_id": order.user_id,
            "total": order.total,
            "product_id": order_product.product_id,
            "quantity": order_product.quantity,
            "product_price": product.price,
            "product_name": product.name,
            "product_image": product.image  
        }
        count_rate_product = db.query(func.count(distinct(models.Rate.product_id))).filter(models.Rate.order_id==order.id).all()
        count_order_product = db.query(func.count(distinct(models.OrderProduct.product_id))).filter(models.OrderProduct.order_id==order.id).all()
        for count_rate, count_product in zip(count_rate_product, count_order_product):
            count_result = {
                "order_id": order.id,
                "count_order_product": count_product[0],
                "count_rate_product": count_rate[0]
            }
            count_check.append(count_result)
        check_last_order = db.query(func.max(models.OrderProduct.id)).filter(models.OrderProduct.order_id == order.id).scalar()
        if check_last_order not in max_order:
            max_order.append(check_last_order)
        data_order.append(get_order)
    for i in max_order:
        check_last_product= db.query(models.OrderProduct.product_id).filter(models.OrderProduct.id == i).first()
        last_product.append(check_last_product)
    get_last_product = [result[0] for result in last_product]
    return {
        "success":True,
        "message":"Thông tin đơn hàng đang vận chuyển !",
        "order": data_order,
        "last_product": get_last_product,
        "check_rate":count_check
    }

def handleOrderCancel(user):
    db=SessionLocal()
    query = (
    db.query(models.Order, models.Product,models.OrderProduct)
    .join(models.OrderProduct, models.Order.id == models.OrderProduct.order_id)
    .join(models.Product, models.OrderProduct.product_id == models.Product.id)
    .filter(models.Order.user_id == user)
    .filter(models.Order.status == 3)
    )
    results = query.all()
    data_order=[]
    last_product=[]
    max_order=[]
    get_last_product=[]
    count_check=[]
    for order, product, order_product in results:
        get_order={
            "id":order.id,
            "payment": order.payment,
            "status": order.status,
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "user_id": order.user_id,
            "total": order.total,
            "product_id": order_product.product_id,
            "quantity": order_product.quantity,
            "product_price": product.price,
            "product_name": product.name,
            "product_image": product.image  
        }
        count_rate_product = db.query(func.count(distinct(models.Rate.product_id))).filter(models.Rate.order_id==order.id).all()
        count_order_product = db.query(func.count(distinct(models.OrderProduct.product_id))).filter(models.OrderProduct.order_id==order.id).all()
        for count_rate, count_product in zip(count_rate_product, count_order_product):
            count_result = {
                "order_id": order.id,
                "count_order_product": count_product[0],
                "count_rate_product": count_rate[0]
            }
            count_check.append(count_result)
        check_last_order = db.query(func.max(models.OrderProduct.id)).filter(models.OrderProduct.order_id == order.id).scalar()
        if check_last_order not in max_order:
            max_order.append(check_last_order)
        data_order.append(get_order)
    for i in max_order:
        check_last_product= db.query(models.OrderProduct.product_id).filter(models.OrderProduct.id == i).first()
        last_product.append(check_last_product)
    get_last_product = [result[0] for result in last_product]
    return {
        "success":True,
        "message":"Thông tin đơn đã hủy !",
        "order": data_order,
        "last_product": get_last_product,
        "check_rate":count_check
    }

def handleUpdateStatus(order_id):
    db=SessionLocal()
    check_order =  db.query(models.Order).filter(models.Order.id==order_id).first()
    if check_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tồn tại đơn hàng !"
        )
    check_order.status=2
    db.commit()
    return {
        "success":True,
        "message":"Xác nhận đã nhận hàng thành công !"
    }
    
def handleCancelOrder(order_id):
    db=SessionLocal()
    check_order =  db.query(models.Order).filter(models.Order.id==order_id).first()
    if check_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Không tồn tại đơn hàng !"
        )
    check_order.status=3
    db.commit()
    return {
        "success":True,
        "message":"Hủy đơn hàng thành công !"
    }

def checkRateProduct(order_id,user_id):
    db=SessionLocal()
    get_rate= db.query(models.Rate).filter(models.Rate.user_id==user_id).filter(models.Rate.order_id==order_id).all()
    return get_rate    
    
def handleOrderRate(user_id,order_id):
    db=SessionLocal()
    query = (
    db.query(models.Order, models.Product,models.OrderProduct)
    .join(models.OrderProduct, models.Order.id == models.OrderProduct.order_id)
    .join(models.Product, models.OrderProduct.product_id == models.Product.id)
    .filter(models.Order.user_id == user_id)
    .filter(models.Order.id == order_id)
    .filter(models.Order.status == 2)
    )
    results = query.all()
    list_data_order=[]
    list_data_rate=[]
    count_check=[]
    for order, product, order_product in results:
        get_order={
            "id":order.id,
            "payment": order.payment,
            "status": order.status,
            "name": order.name,
            "address": order.address,
            "phone": order.phone,
            "user_id": order.user_id,
            "total": order.total,
            "product_id": order_product.product_id,
            "quantity": order_product.quantity,
            "product_price": product.price,
            "product_name": product.name,
            "product_image": product.image  
        }
        count_rate_product = db.query(func.count(distinct(models.Rate.product_id))).filter(models.Rate.order_id==order.id).all()
        count_order_product = db.query(func.count(distinct(models.OrderProduct.product_id))).filter(models.OrderProduct.order_id==order.id).all()
        for count_rate, count_product in zip(count_rate_product, count_order_product):
            count_result = {
                "order_id": order.id,
                "count_order_product": count_product[0],
                "count_rate_product": count_rate[0]
            }
            count_check.append(count_result)
        data_rate_order=checkRateProduct(order.id,order.user_id)
        if len(data_rate_order)>0:
            for rate in data_rate_order:
                get_rate_order={
                    "id": rate.id,
                    "product_id": rate.product_id,
                    "user_id": rate.user_id,
                    "star": rate.star,
                    "comment": rate.comment,
                }
            list_data_rate.append(get_rate_order)    
        list_data_order.append(get_order)
    return {
        "success":True,
        "order": list_data_order,
        "get_rate": list_data_rate
    }
    