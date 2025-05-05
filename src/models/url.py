from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from ..utils.database.postgres import postgresql_database


class Url(postgresql_database.base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, nullable=False)
    short_url = Column(String, unique=True, nullable=False)
    calls = Column(Integer, default=0, nullable=False)
    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )
