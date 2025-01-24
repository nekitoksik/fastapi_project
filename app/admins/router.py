from fastapi import APIRouter, Response
from app.exceptions import IncorrectUserEmailOrPasswordException, UserAlreadyExcist

from app.admins.models import Admins
from app.admins.services import AdminService
from app.admins.schemas import SAdminAuth
from app.admins.auth import get_password_hash, verify_password, create_access_token, verify_user


router = APIRouter(
    prefix='/admin',
    tags=['Админы'],
)

@router.post("/register")
async def register_admin(admin_data: SAdminAuth):

    existing_admin = await AdminService.find_one_or_none(email=admin_data.email)

    if existing_admin:
        raise UserAlreadyExcist
    
    hashed_password = get_password_hash(admin_data.password)
    await AdminService.add(email=admin_data.email, password=hashed_password)


@router.post("/login")
async def login_user(response: Response, admin_data: SAdminAuth):
    
    admin = await verify_user(admin_data.email, admin_data.password)
    if not admin:
        raise IncorrectUserEmailOrPasswordException
    access_token = create_access_token({"sub": str(admin.id)})    
    response.set_cookie("tatrun_token", access_token, httponly=True)
    return access_token



@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("tatrun_token")