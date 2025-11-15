import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
from pgvector.sqlalchemy import Vector

from app.db.database import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False
    )

    # Metadata
    article_ref = Column(String, nullable=True)

    #Clean text of the chunk (silver layer asset)
    text = Column(String, nullable=False)

    # Embedding (gold layer)
    embedding = Column(Vector(1536)) # Assuming OpenAI's embedding size

    # Risk laels assigned by the classifier 
    risk_labels = Column(ARRAY(String), nullable=True)

    #Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")