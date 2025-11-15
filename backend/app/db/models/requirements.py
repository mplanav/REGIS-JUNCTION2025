from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from .enums import RiskTypeEnum, JurisdictionEnum


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    page = Column(Integer, nullable=True)
    line = Column(Integer, nullable=True)

    risk_type = Column(Enum(RiskTypeEnum, name="risk_type_enum"), nullable=False, index=True)
    jurisdiction = Column(String, nullable=False, index=True)

    contradictions_as_first = relationship("Contradiction", back_populates="requirement1",
                                          foreign_keys="Contradiction.requirement1_id")
    contradictions_as_second = relationship("Contradiction", back_populates="requirement2",
                                           foreign_keys="Contradiction.requirement2_id")

    overlaps_as_first = relationship("Overlap", back_populates="requirement1",
                                     foreign_keys="Overlap.requirement1_id")
    overlaps_as_second = relationship("Overlap", back_populates="requirement2",
                                      foreign_keys="Overlap.requirement2_id")


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(Integer, primary_key=True, index=True)
    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    description = Column(Text, nullable=True)
    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)
    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship("Requirement", foreign_keys=[requirement1_id], back_populates="contradictions_as_first")
    requirement2 = relationship("Requirement", foreign_keys=[requirement2_id], back_populates="contradictions_as_second")


class Overlap(Base):
    __tablename__ = "overlaps"

    id = Column(Integer, primary_key=True, index=True)
    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    reason = Column(Text, nullable=True)

    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)
    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship("Requirement", foreign_keys=[requirement1_id], back_populates="overlaps_as_first")
    requirement2 = relationship("Requirement", foreign_keys=[requirement2_id], back_populates="overlaps_as_second")


class RequirementEmbedding(Base):
    __tablename__ = "requirement_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), unique=True, nullable=False)
    embedding = Column(Text, nullable=False)

    requirement = relationship("Requirement")
