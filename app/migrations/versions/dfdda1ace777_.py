"""empty message

Revision ID: dfdda1ace777
Revises: 
Create Date: 2025-02-03 21:45:26.591471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfdda1ace777'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_admins_id'), 'admins', ['id'], unique=False)
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_type', sa.Enum('DAILY', 'ONE_TIME', name='tasktype'), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('target_type', sa.Enum('FRIEND', 'STEPS', 'KILOMETER', name='targettype'), nullable=False),
    sa.Column('target_value', sa.Integer(), nullable=True),
    sa.Column('reward', sa.Integer(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('phone_number', sa.String(length=20), nullable=False),
    sa.Column('verification_code', sa.String(length=6), nullable=True),
    sa.Column('code_expires_at', sa.DateTime(), nullable=True),
    sa.Column('jwt_token', sa.String(length=500), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('photo_url', sa.String(length=255), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('about', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('steps', sa.Integer(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('friendships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requester_id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'ACCEPTED', 'REJECTED', name='friendshipstatus'), nullable=True),
    sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_friendships_id'), 'friendships', ['id'], unique=False)
    op.create_table('run_stats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=True),
    sa.Column('steps', sa.Integer(), nullable=True),
    sa.Column('calories_burned', sa.Float(), nullable=True),
    sa.Column('average_speed', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_run_stats_id'), 'run_stats', ['id'], unique=False)
    op.create_table('user_task_progress',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=True),
    sa.Column('completed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_task_progress_id'), 'user_task_progress', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_task_progress_id'), table_name='user_task_progress')
    op.drop_table('user_task_progress')
    op.drop_index(op.f('ix_run_stats_id'), table_name='run_stats')
    op.drop_table('run_stats')
    op.drop_index(op.f('ix_friendships_id'), table_name='friendships')
    op.drop_table('friendships')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_admins_id'), table_name='admins')
    op.drop_table('admins')
    # ### end Alembic commands ###
