from fastapi import APIRouter, HTTPException, status,File, UploadFile
from controllers import AuthController,ContactController
from pydantic import BaseModel
import models

router=APIRouter()

class UserRegister(BaseModel):
    name: str
    email: str
    username: str
    password: str
    class Config:
        arbitrary_types_allowed = True

class UserLogin(BaseModel):
    username: str
    password: str
    class Config:
        arbitrary_types_allowed = True

@router.post("/api/v1/login",status_code=status.HTTP_200_OK)
def loginUser(user:UserLogin):
    try:
        data_user = models.User(**user.dict())
        data= AuthController.loginUser(data_user)
        print(data)
        return data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )

@router.post("/api/v1/register",status_code=status.HTTP_200_OK)
def registerUser(user:UserRegister):
    try:
        data_user = models.User(**user.dict())
        data= AuthController.registerUser(data_user)
        print(data)
        return data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )
        
class SendMail(BaseModel):
    name:str
    title:str
    email:str
    content:str
    # file: UploadFile = File(...)

@router.post("/api/v1/send",status_code=status.HTTP_200_OK)
def registerUser(data:SendMail):
    try:
      
        data= ContactController.handleSendMail(data)
        print(data)
        return data
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )