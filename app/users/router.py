from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from typing import Optional
from app.users.schemas import SUser, SUserCreate, SUserUpdate, PhoneRequest, VerifyCodeRequest
from app.users.services import UserService
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)

@router.get("")
async def get_users() -> list[SUser]:
    result = await UserService.get_all()
    return result

@router.patch("/me", response_model=SUserUpdate)
async def update_user(
    update_data: SUserUpdate,
    token: str
):

    try:
        return await UserService.update_user(token, update_data)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/get-me")
async def read_users_me(token: str, current_user: Users = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "phone": current_user.phone_number,
        "points": current_user.points,
        "steps": current_user.steps
    }


@router.get("/{user_id}")
async def get_user_by_id(user_id: int) -> SUser:
    user = await UserService.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", response_model=SUser, status_code=201)
async def create_user(
    name: str = Form(...),
    phone_number = Form(...),
    height: int = Form(...),
    weight: int = Form(...),
    about: str = Form(...),
    city: str = Form(...),
    steps: int = Form(...),
    photo: UploadFile = File(None)
) -> SUser:
    
    
    if await UserService.check_phone_unique(phone_number):

        user_data = SUserCreate(
            name=name,
            phone_number=phone_number,
            height=height,
            weight=weight,
            about=about,
            city=city,
            steps=steps
        )

        return await UserService.create_user(user_data, photo)

    else:
        raise HTTPException(
                status_code=400,
                detail="Пользователь с таким номером уже зарегистрирован"
            )

@router.post("/logout")
async def logout(current_user: Users = Depends(get_current_user)):
    await UserService.logout_user(current_user)
    return {"status": "success"}

@router.put("/users/upload_photo", response_model=SUser)
async def upload_photo(
    photo: UploadFile = File(...),
    current_user: Users = Depends(get_current_user)
) -> SUser:
    return await UserService.upload_user_photo(current_user, photo)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    await UserService.delete_user(user_id)
    return {}


@router.post("/{user_id}/add-points", response_model=SUser)
async def add_points(user_id: int, points_to_add: int):
    
    try:
        user = await UserService.add_points_to_user(user_id, points_to_add)
        return user
    except HTTPException as e:
        raise e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/{user_id}/add-steps", response_model=SUser)
async def add_steps(user_id: int, steps_to_add: int):

    try:
        user = await UserService.add_steps_to_user(user_id, steps_to_add)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/send-code")
async def send_code(request: PhoneRequest):
    return await UserService.send_verification_code(request.phone)

@router.post("/verify-code")
async def verify_code(request: VerifyCodeRequest):
    return await UserService.verify_code(request.phone, request.code)

