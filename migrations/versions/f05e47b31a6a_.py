"""empty message

Revision ID: f05e47b31a6a
Revises: 1a73c309adda
Create Date: 2023-02-08 07:42:55.388974

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f05e47b31a6a'
down_revision = '1a73c309adda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contacts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('events',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=120), nullable=False),
    sa.Column('date', sa.String(length=120), nullable=False),
    sa.Column('time', sa.String(length=120), nullable=False),
    sa.Column('description', sa.String(length=360), nullable=False),
    sa.Column('location', sa.String(length=240), nullable=False),
    sa.Column('image', sa.String(length=360), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_guests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['contact_id'], ['contacts.id'], ),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('phone', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('city', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('country', sa.String(length=120), nullable=False))
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False))
        batch_op.drop_column('country')
        batch_op.drop_column('city')
        batch_op.drop_column('phone')
        batch_op.drop_column('name')

    op.drop_table('event_guests')
    op.drop_table('events')
    op.drop_table('contacts')
    # ### end Alembic commands ###