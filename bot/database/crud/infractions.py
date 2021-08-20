import typing
from sqlalchemy.orm import Session
from bot.database.models import Infraction


class InfractionDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_infraction(
        self,
        id: int,
        user: str,
        type: str,
        reason: str,
        date: str,
        expires: str,
    ) -> None:
        new_infraction = Infraction(
            id=id, user=user, type=type, reason=reason, date=date, expires=expires
        )
        self.db_session.add(new_infraction)
        await self.db_session.flush()
