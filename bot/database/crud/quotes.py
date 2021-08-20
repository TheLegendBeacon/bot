import typing
from sqlalchemy.orm import Session
from bot.database.models import Quote


class QuoteDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def add_quote(self, id: int, user: str, quote: str) -> None:
        new_quote = Quote(id=id, user=user, quote=quote)
        self.db_session.add(new_quote)
        await self.db_session.flush()
