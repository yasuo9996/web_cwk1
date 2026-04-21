"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-04-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tracks",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("artist", sa.String(length=255), nullable=False),
        sa.Column("album", sa.String(length=255), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("popularity", sa.Integer(), nullable=True),
        sa.Column("danceability", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("energy", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("loudness", sa.Float(), nullable=True),
        sa.Column("valence", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("acousticness", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("tempo", sa.Float(), nullable=True),
        sa.CheckConstraint("danceability >= 0 AND danceability <= 1", name="chk_danceability_range"),
        sa.CheckConstraint("energy >= 0 AND energy <= 1", name="chk_energy_range"),
        sa.CheckConstraint("valence >= 0 AND valence <= 1", name="chk_valence_range"),
        sa.CheckConstraint("acousticness >= 0 AND acousticness <= 1", name="chk_acousticness_range"),
    )
    op.create_index("ix_tracks_id", "tracks", ["id"], unique=False)

    op.create_table(
        "user_profiles",
        sa.Column("user_id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("preferred_energy_min", sa.Float(), nullable=True),
        sa.Column("preferred_energy_max", sa.Float(), nullable=True),
        sa.Column("preferred_danceability_min", sa.Float(), nullable=True),
        sa.Column("preferred_danceability_max", sa.Float(), nullable=True),
        sa.Column("avg_tempo", sa.Float(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=True),
    )
    op.create_index("ix_user_profiles_user_id", "user_profiles", ["user_id"], unique=False)

    op.create_table(
        "listening_records",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("track_id", sa.Integer(), nullable=False),
        sa.Column("listened_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("action_type", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(["track_id"], ["tracks.id"]),
    )
    op.create_index("ix_listening_records_id", "listening_records", ["id"], unique=False)
    op.create_index("ix_listening_records_track_id", "listening_records", ["track_id"], unique=False)
    op.create_index("ix_listening_records_user_id", "listening_records", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_listening_records_user_id", table_name="listening_records")
    op.drop_index("ix_listening_records_track_id", table_name="listening_records")
    op.drop_index("ix_listening_records_id", table_name="listening_records")
    op.drop_table("listening_records")

    op.drop_index("ix_user_profiles_user_id", table_name="user_profiles")
    op.drop_table("user_profiles")

    op.drop_index("ix_tracks_id", table_name="tracks")
    op.drop_table("tracks")
