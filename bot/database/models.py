from sqlalchemy import Column, Integer, String, TIMESTAMP

from bot.database.database import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    quote = Column(String, nullable=False)


class Infraction(Base):
    __tablename__ = "infractions"

    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    type = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    date = Column(TIMESTAMP, nullable=False)
    expires = Column(TIMESTAMP, nullable=False)
