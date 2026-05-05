from sqlalchemy import Column,Integer,String,Float,Boolean,DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class ModerationLog(Base):
    __tablename__="moderation_logs"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    is_flagged = Column(Boolean,default=False)
    toxicity_score = Column(Float)
    category = Column(String)
    created_at = Column(DateTime(timezone=True),server_default=func.now())