import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, JSON, DateTime, String
from db.database import db

class Idea(db.Model):
    __tablename__ = 'ideas'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False) # Will store JSON of StructuredIdeaInput
    status: Mapped[str] = mapped_column(String(50), default="pending")
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
    
class Report(db.Model):
    __tablename__ = 'reports'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    idea_id: Mapped[int] = mapped_column(nullable=False)
    structured_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    scores: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )
