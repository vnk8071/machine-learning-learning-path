"""empty message

Revision ID: 256536967864
Revises: b0822bf0ee03
Create Date: 2023-10-05 14:47:17.471513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256536967864'
down_revision = 'b0822bf0ee03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artists',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=200), nullable=True),
                    sa.Column('state', sa.String(length=200), nullable=True),
                    sa.Column('phone', sa.String(length=200), nullable=True),
                    sa.Column('genres', sa.String(length=200), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(length=200), nullable=True),
                    sa.Column('website_link', sa.String(), nullable=True),
                    sa.Column('seeking_venue', sa.Boolean(), nullable=False),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('venues',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('city', sa.String(length=200), nullable=True),
                    sa.Column('state', sa.String(length=200), nullable=True),
                    sa.Column('address', sa.String(length=200), nullable=True),
                    sa.Column('phone', sa.String(length=200), nullable=True),
                    sa.Column('image_link', sa.String(length=500), nullable=True),
                    sa.Column('facebook_link', sa.String(length=200), nullable=True),
                    sa.Column('seeking_talent', sa.Boolean(), nullable=False),
                    sa.Column('seeking_description', sa.String(), nullable=True),
                    sa.Column('website_link', sa.String(), nullable=True),
                    sa.Column('genres', sa.String(length=200), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('shows',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('start_time', sa.DateTime(), nullable=False),
                    sa.Column('artist_id', sa.Integer(), nullable=False),
                    sa.Column('venue_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['artist_id'], ['artists.id'], ),
                    sa.ForeignKeyConstraint(['venue_id'], ['venues.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shows')
    op.drop_table('venues')
    op.drop_table('artists')
    # ### end Alembic commands ###
