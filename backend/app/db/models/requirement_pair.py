import uuid
from sqlalchemy import Column, String, Float, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.database import Base


class RequirementPair(Base):
    __tablename__ = "requirement_pairs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    chunk_a_id = Column(UUID(as_uuid=True), ForeignKey("chunks.id"))
    chunk_b_id = Column(UUID(as_uuid=True), ForeignKey("chunks.id"))

    # NLI Results
    relation = Column(String)  # "contradiction", "entailment", "neutral"
    confidence = Column(Float)

    # Optional summary of the conflict
    explanation = Column(String, nullable=True)

    # Flags
    is_active = Column(Boolean, default=True)

    # Relations back to chunks
    chunk_a = relationship("Chunk", foreign_keys=[chunk_a_id])
    chunk_b = relationship("Chunk", foreign_keys=[chunk_b_id])
