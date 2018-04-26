"""empty message

Revision ID: 23bc2160af2e
Revises: 
Create Date: 2018-04-24 21:24:16.948793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23bc2160af2e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_name'), 'categories', ['name'], unique=False)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_name'), 'tags', ['name'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('clubs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('snippet', sa.String(length=500), nullable=True),
    sa.Column('description', sa.String(length=10000), nullable=True),
    sa.Column('leader', sa.String(length=150), nullable=True),
    sa.Column('price', sa.String(length=50), nullable=True),
    sa.Column('phone', sa.String(length=30), nullable=True),
    sa.Column('web', sa.String(length=100), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('social', sa.String(length=100), nullable=True),
    sa.Column('street', sa.String(length=30), nullable=True),
    sa.Column('building', sa.String(length=10), nullable=True),
    sa.Column('room', sa.String(length=5), nullable=True),
    sa.Column('days', sa.String(length=50), nullable=True),
    sa.Column('start', sa.String(length=50), nullable=True),
    sa.Column('finish', sa.String(length=50), nullable=True),
    sa.Column('url_logo', sa.String(length=300), nullable=True),
    sa.Column('reg_date', sa.DateTime(), nullable=True),
    sa.Column('last_edit_date', sa.DateTime(), nullable=True),
    sa.Column('institution', sa.String(length=300), nullable=True),
    sa.Column('ages_from', sa.Integer(), nullable=True),
    sa.Column('ages_to', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_clubs_last_edit_date'), 'clubs', ['last_edit_date'], unique=False)
    op.create_index(op.f('ix_clubs_name'), 'clubs', ['name'], unique=False)
    op.create_index(op.f('ix_clubs_reg_date'), 'clubs', ['reg_date'], unique=False)
    op.create_index(op.f('ix_clubs_state'), 'clubs', ['state'], unique=False)
    op.create_table('association_categories',
    sa.Column('clubs_id', sa.Integer(), nullable=True),
    sa.Column('categories_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['categories_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['clubs_id'], ['clubs.id'], )
    )
    op.create_table('association_tags',
    sa.Column('clubs_id', sa.Integer(), nullable=True),
    sa.Column('tags_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['clubs_id'], ['clubs.id'], ),
    sa.ForeignKeyConstraint(['tags_id'], ['tags.id'], )
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=300), nullable=True),
    sa.Column('club_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['club_id'], ['clubs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photos')
    op.drop_table('association_tags')
    op.drop_table('association_categories')
    op.drop_index(op.f('ix_clubs_state'), table_name='clubs')
    op.drop_index(op.f('ix_clubs_reg_date'), table_name='clubs')
    op.drop_index(op.f('ix_clubs_name'), table_name='clubs')
    op.drop_index(op.f('ix_clubs_last_edit_date'), table_name='clubs')
    op.drop_table('clubs')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tags_name'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_categories_name'), table_name='categories')
    op.drop_table('categories')
    # ### end Alembic commands ###
