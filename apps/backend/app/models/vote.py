"""ArenaVote model storing audience spectator votes with Sybil resistance."""

import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ArenaVote(Base):
    """A spectator vote cast for an agent in a match."""

    __tablename__ = "arena_votes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    match_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("arena_matches.id", ondelete="CASCADE"), nullable=False, index=True)
    voter_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    voted_agent_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("agents.id"), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("match_id", "voter_user_id", name="uq_match_user_vote"),
    )

    # Relationships
    match = relationship("ArenaMatch", back_populates="votes")
    voter = relationship("User", back_populates="votes")
