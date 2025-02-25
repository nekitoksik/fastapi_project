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

            # Проверяем существующую запись в базе данных
            existing_relationship = await session.execute(
                select(Friendship).filter(
                    (Friendship.recipient_id == recipient_id) & (Friendship.requester_id == requester_id) |
                    (Friendship.recipient_id == requester_id) & (Friendship.requester_id == recipient_id)
                )
            )
            existing_relationship = existing_relationship.scalar_one_or_none()

            if existing_relationship:
                if existing_relationship.status == FriendshipStatus.PENDING:
                    return {"message": "Friend request already sent"}
                elif existing_relationship.status == FriendshipStatus.ACCEPTED:
                    return {"message": "Users are already friends"}
                elif existing_relationship.status == FriendshipStatus.REJECTED:
                    # Если запись была отклонена, обновляем её статус на PENDING
                    existing_relationship.status = FriendshipStatus.PENDING
                    await session.commit()
                    await session.refresh(existing_relationship)
                    return {"message": "Friend request resent"}
            else:
                # Если записи нет, создаем новую
                new_friendship = Friendship(
                    requester_id=requester_id, recipient_id=recipient_id
                )
                session.add(new_friendship)
                await session.commit()
                await session.refresh(new_friendship)
                return {"message": "Friend request sent"}

    @classmethod
    async def get_pending_friend_requests(cls, user_id: int) -> list[FriendSchema]:
        """Возвращает список предложений в друзья для пользователя со статусом PENDING."""
        async with async_session_maker() as session:
            user = await session.get(Users, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            pending_requests = await session.execute(
                select(Users)
                .join(Friendship, Users.id == Friendship.requester_id)
                .filter(
                    Friendship.recipient_id == user_id,
                    Friendship.status == FriendshipStatus.PENDING,
                )
            )
            pending_requests = pending_requests.scalars().all()

            return [
                FriendSchema(
                    id=friend.id,
                    name=friend.name,
                    photo_url=friend.photo_url,
                    city=friend.city,
                    steps=friend.steps,
                    points=friend.points,
                )
                for friend in pending_requests
            ]

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
        
    @classmethod
    async def accept_friend_request(cls, user_id: int, friend_id: int):
        async with async_session_maker() as session:

            user = await session.get(Users, user_id)
            friend = await session.get(Users, friend_id)

            if user_id == friend_id:
                raise HTTPException(status_code=404, detail="User id and Friend id is equal!")
            elif not user or not friend:
                raise HTTPException(status_code=404, detail="User or friend not found")

            friends = await session.execute(select(Friendship).filter(
                Friendship.requester_id == friend_id,
                Friendship.recipient_id == user_id
            ))

            friends = friends.scalars().first()

            if friends:
                if friends.status in [FriendshipStatus.PENDING, FriendshipStatus.REJECTED]:
                    friends.status = FriendshipStatus.ACCEPTED
                    await session.commit()
                    return "Друг добавлен! Статус изменен"
                else:
                    return "Статус дружбы уже принят или отклонен."
            else:
                return "Запись о дружбе не найдена."
            
    @classmethod
    async def delete_from_friends(cls, user_id: int, friend_id: int):
        async with async_session_maker() as session:

            user = await session.get(Users, user_id)
            friend = await session.get(Users, friend_id)

            if user_id == friend_id:
                raise HTTPException(status_code=404, detail="User id and Friend id is equal!")
            elif not user:
                raise HTTPException(status_code=404, detail="User not found")
            elif not friend:
                raise HTTPException(status_code=404, detail="friend not found")
            
            friends = await session.execute(select(Friendship).filter(
                (Friendship.requester_id == friend_id) & (Friendship.recipient_id == user_id) |
                (Friendship.recipient_id == friend_id) & (Friendship.requester_id == user_id)
            ))

            friends = friends.scalars().first()

            if friends:
                if friends.status in [FriendshipStatus.ACCEPTED, FriendshipStatus.REJECTED]:
                    friends.status = FriendshipStatus.REJECTED
                    await session.commit()
                    return "Пользователь удален из друзей!"
                else:
                    return "Пользователь не является вашим другом"
            else:
                return "Запись о дружбе не найдена."
            

    
    @classmethod
    async def reject_friend_request(cls, user_id: int, requester_id: int):
        async with async_session_maker() as session:

            user = await session.get(Users, user_id)
            requester = await session.get(Users, requester_id)


            if user_id == requester_id:
                raise HTTPException(status_code=404, detail="User id and Requester id is equal!")
            elif not user:
                raise HTTPException(status_code=404, detail="User not found")
            elif not requester:
                raise HTTPException(status_code=404, detail="Requester not found")
            
            friends = await session.execute(select(Friendship).filter(
                Friendship.requester_id == requester_id,
                Friendship.recipient_id == user_id
            ))

            friends = friends.scalars().first()

            if friends:
                if friends.status in [FriendshipStatus.PENDING]:
                    friends.status = FriendshipStatus.REJECTED
                    await session.commit()
                    return "Запрос о дружбе отклонен"
                else:
                    return "Статус дружбы уже принят или отклонен."
            else:
                return "Запись о дружбе не найдена."