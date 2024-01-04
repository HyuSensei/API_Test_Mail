from fastapi import APIRouter, HTTPException, status
from controllers.user import AuthController
import models
from pydantic import BaseModel

router=APIRouter()

class UserRegisterBase(BaseModel):
    name: str
    email: str
    username: str
    password: str
    address: str
    role_id: int
    class Config:
        arbitrary_types_allowed = True

class UserLogin(BaseModel):
    username: str
    password: str
    class Config:
        arbitrary_types_allowed = True

@router.post("/api/v1/register",status_code=status.HTTP_201_CREATED)
def registerUser(user: UserRegisterBase):
    try:
        data_user = models.User(**user.dict())
        db_user = AuthController.registerUser(data_user)
        print(db_user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
        
@router.post("/api/v1/login",status_code=status.HTTP_200_OK)
def loginUser(user:UserLogin):
    try:
        data_user=models.User(**user.dict())
        get_data= AuthController.loginUser(data_user)
        print(get_data)
        return get_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
        
@router.get("/api/v1/authenticate/{token}",status_code=status.HTTP_200_OK)
def authLogin(token:str):
    try:
        get_data= AuthController.authLoginUser(token)
        print(get_data)
        return get_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.get("/api/v1/users/{user_id}",status_code=status.HTTP_200_OK)
def getUserLogin(user_id:int):
    try:
        get_data= AuthController.handleGetUserLogin(user_id)
        print(get_data)
        return get_data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
    