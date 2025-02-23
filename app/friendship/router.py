from fastapi import APIRouter, status

from app.friendship.schemas import FriendSchema
from app.friendship.services import FriendServices

router = APIRouter(
    prefix="/friends",
    tags=["Друзья"],
)

@router.get("/{user_id}/", response_model=list[FriendSchema])
async def get_friends(user_id: int):
    return await FriendServices.get_accepted_friend_ids(user_id)


@router.post("/send_request", status_code=status.HTTP_201_CREATED)
async def send_friend_request(requester_id: int, recipient_id: int):
    result = await FriendServices.send_friend_request(requester_id, recipient_id)
    return result

@router.post("/accept")
async def accept_friend_request(user_id: int, friend_id: int):

    return await FriendServices.accept_friend_request(user_id, friend_id)

@router.get("/{user_id}/pending-requests", response_model=list[FriendSchema])
async def get_pending_friend_requests(user_id: int):
    return await FriendServices.get_pending_friend_requests(user_id)

@router.post("/delete")
async def delete_friend(user_id: int, friend_id: int):

    return await FriendServices.delete_from_friends(user_id, friend_id)


@router.patch("/reject_request")
async def reject_friend_request(user_id: int, requester_id: int):

    return await FriendServices.reject_friend_request(user_id, requester_id)