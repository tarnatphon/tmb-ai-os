"""Initial canonical schema."""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "content_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("topic", sa.String(255), nullable=False),
        sa.Column("pillar", sa.String(120), nullable=False),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("prompt_hash", sa.String(64), nullable=True),
    )
    op.create_index(
        "ix_content_runs_prompt_hash",
        "content_runs",
        ["prompt_hash"],
        unique=True,
    )
    op.create_table(
        "content_audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "content_id",
            sa.Integer(),
            sa.ForeignKey("content_runs.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("actor", sa.String(120), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "publish_queue",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "content_id",
            sa.Integer(),
            sa.ForeignKey("content_runs.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("status", sa.String(50), nullable=False),
        sa.Column("scheduled_for", sa.DateTime(timezone=True), nullable=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_table(
        "security_audit_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("actor", sa.String(120), nullable=False),
        sa.Column("role", sa.String(50), nullable=False),
        sa.Column("action", sa.String(120), nullable=False),
        sa.Column("outcome", sa.String(50), nullable=False),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("security_audit_events")
    op.drop_table("publish_queue")
    op.drop_table("content_audit_events")
    op.drop_table("content_runs")
