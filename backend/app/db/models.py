# app/db/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base
import enum


# --- Enums ---

class RiskTypeEnum(str, enum.Enum):
    AML = "AML"
    FRAUD = "FRAUD"
    CYBERSECURITY = "CYBERSECURITY"
    GOVERNANCE = "GOVERNANCE"
    PRIVACY = "PRIVACY"
    OPERATIONAL = "OPERATIONAL"
    COMPLIANCE = "COMPLIANCE"
    OTHER = "OTHER"


# Si luego hay más jurisdicciones en gold.zip, podemos dejarlas como texto libre,
# pero definimos las más usadas como referencia.
class JurisdictionEnum(str, enum.Enum):
    EU = "EU"
    FINLAND = "FINLAND"
    GLOBAL = "GLOBAL"
    OTHER = "OTHER"


# --- Models ---

class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True, index=True)

    # Texto del requerimiento / riesgo
    text = Column(Text, nullable=False)

    # Página y línea en el documento
    page = Column(Integer, nullable=True)
    line = Column(Integer, nullable=True)

    # Tipo de riesgo
    risk_type = Column(
        Enum(RiskTypeEnum, name="risk_type_enum"),
        nullable=False,
        index=True,
    )

    # Jurisdicción (EU, FINLAND, GLOBAL, etc.)
    jurisdiction = Column(
        String,
        nullable=False,
        index=True,
        default=JurisdictionEnum.GLOBAL.value,
    )

    # Relaciones para navegar desde requirement -> contradictions/overlaps
    contradictions_as_first = relationship(
        "Contradiction",
        back_populates="requirement1",
        foreign_keys="Contradiction.requirement1_id",
    )
    contradictions_as_second = relationship(
        "Contradiction",
        back_populates="requirement2",
        foreign_keys="Contradiction.requirement2_id",
    )

    overlaps_as_first = relationship(
        "Overlap",
        back_populates="requirement1",
        foreign_keys="Overlap.requirement1_id",
    )
    overlaps_as_second = relationship(
        "Overlap",
        back_populates="requirement2",
        foreign_keys="Overlap.requirement2_id",
    )


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(Integer, primary_key=True, index=True)

    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)

    # Descripción corta de por qué se contradicen
    description = Column(Text, nullable=True)

    # Posiciones en el documento
    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)

    # Opcional: jurisdicción principal afectada
    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship(
        "Requirement",
        back_populates="contradictions_as_first",
        foreign_keys=[requirement1_id],
    )
    requirement2 = relationship(
        "Requirement",
        back_populates="contradictions_as_second",
        foreign_keys=[requirement2_id],
    )


class Overlap(Base):
    __tablename__ = "overlaps"

    id = Column(Integer, primary_key=True, index=True)

    requirement1_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)
    requirement2_id = Column(Integer, ForeignKey("requirements.id"), nullable=False)

    # Por qué se solapan (similaridad, duplicidad, etc.)
    reason = Column(Text, nullable=True)

    # Posiciones en el documento
    page_1 = Column(Integer, nullable=True)
    line_1 = Column(Integer, nullable=True)
    page_2 = Column(Integer, nullable=True)
    line_2 = Column(Integer, nullable=True)

    jurisdiction = Column(String, nullable=True, index=True)

    requirement1 = relationship(
        "Requirement",
        back_populates="overlaps_as_first",
        foreign_keys=[requirement1_id],
    )
    requirement2 = relationship(
        "Requirement",
        back_populates="overlaps_as_second",
        foreign_keys=[requirement2_id],
    )

class RequirementEmbedding(Base):
    __tablename__ = "requirement_embeddings"

    id = Column(Integer, primary_key=True, index=True)
    requirement_id = Column(Integer, ForeignKey("requirements.id"), unique=True, nullable=False)

    # Guardamos el embedding como JSON string (lista de floats serializada)
    embedding = Column(Text, nullable=False)

    requirement = relationship("Requirement")


