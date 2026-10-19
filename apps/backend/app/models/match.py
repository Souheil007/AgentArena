"""ArenaMatch model representing live and completed agent matches."""

import enum
import uuid
from datetime import datetime
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MatchStatus(str, enum.Enum):
    """Lifecycle states of an arena match."""
    WAITING_FOR_OPPONENT = "WAITING_FOR_OPPONENT"
    IN_PROGRESS = "IN_PROGRESS"
    VOTING = "VOTING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ArenaMatch(Base):
    """An active or completed head-to-head duel between two agents."""

    __tablename__ = "arena_matches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("arena_challenges.id"), nullable=False, index=True)
    
    agent_a_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False, index=True)
    agent_b_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True, index=True)
    
    status: Mapped[MatchStatus] = mapped_column(Enum(MatchStatus), default=MatchStatus.WAITING_FOR_OPPONENT, index=True, nullable=False)
    
    # Voting results (anonymized during battle)
    votes_agent_a: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    votes_agent_b: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    winner_agent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=True)
    elo_delta_a: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    elo_delta_b: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    challenge = relationship("ArenaChallenge", back_populates="matches")
    turns = relationship("ArenaTurn", back_populates="match", cascade="all, delete-orphan", order_by="ArenaTurn.turn_index")
    votes = relationship("ArenaVote", back_populates="match", cascade="all, delete-orphan")
