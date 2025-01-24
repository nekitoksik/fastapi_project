from fastapi import HTTPException
from app.users.models import Friendship, Users, FriendshipStatus
from app.services.base import BaseService

from app.friendship.schemas import FriendSchema, FriendRequestSchema

from app.database import async_session_maker
from sqlalchemy import select, delete, exists
from sqlalchemy.orm import selectinload, joinedload

class FriendServices(BaseService):
    model = Users
    
    @classmethod
    async def send_friend_request(cls, requester_id: int, recipient_id: int):
        async with async_session_maker() as session:

            requester = await session.get(Users, requester_id)
            recipient = await session.get(Users, recipient_id)

            if not recipient or not requester:
                raise HTTPException(status_code=404, detail="User not found")
            


            existing_relationship = await session.execute(
                select(Friendship.status).filter(
                    (Friendship.recipient_id == recipient_id) & (Friendship.requester_id == requester_id) |
                    (Friendship.recipient_id == requester_id) & (Friendship.requester_id == recipient_id)
                )
            )

            existing_relationship = existing_relationship.scalar_one_or_none()
            print(existing_relationship)

            if existing_relationship == FriendshipStatus.PENDING:
                return {"message": "Friend request already sent"}
            elif existing_relationship == FriendshipStatus.ACCEPTED:
                return {"message": "Users are already friends"}
            elif existing_relationship == FriendshipStatus.REJECTED:
                pass
            

            new_friendship = Friendship(
                requester_id=requester_id, recipient_id=recipient_id
            )
            session.add(new_friendship)
            await session.commit()
            await session.refresh(new_friendship)
    
    @classmethod
    async def get_accepted_friend_ids(cls, user_id: int) -> list[FriendSchema]:
        """Возвращает список ID друзей пользователя со статусом ACCEPTED."""
        async with async_session_maker() as session:
            user = await session.get(Users, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            friends1 = await session.execute(
                select(Users)
                .join(Friendship, Users.id == Friendship.recipient_id)
                .filter(
                    Friendship.requester_id == user_id,
                    Friendship.status == FriendshipStatus.ACCEPTED,
                )
            )
            friends1 = friends1.scalars().all()


            friends2 = await session.execute(
                select(Users)
                .join(Friendship, Users.id == Friendship.requester_id)  # Join по requester_id
                .filter(
                    Friendship.recipient_id == user_id,  # recipient_id == user_id
                    Friendship.status == FriendshipStatus.ACCEPTED,
                )
            )
            friends2 = friends2.scalars().all()

            all_friends = list(set(friends1 + friends2))

            return [
                FriendSchema(
                    id=friend.id,
                    name=friend.name,
                    photo_url=friend.photo_url,
                    city=friend.city,
                    steps=friend.steps,
                    points=friend.points,
                )
                for friend in all_friends
            ]