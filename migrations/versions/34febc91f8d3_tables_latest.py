"""tables latest

Revision ID: 34febc91f8d3
Revises: 60a6b4a2da51
Create Date: 2020-09-28 04:31:32.381785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34febc91f8d3'
down_revision = '60a6b4a2da51'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('AccountInfo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('numFollowing', sa.Integer(), nullable=True),
    sa.Column('numFollowers', sa.Integer(), nullable=True),
    sa.Column('numPosts', sa.Integer(), nullable=True),
    sa.Column('numDailyVisits', sa.Integer(), nullable=True),
    sa.Column('numDailyFollowers', sa.Integer(), nullable=True),
    sa.Column('numDailyReach', sa.Integer(), nullable=True),
    sa.Column('numDailyImpressions', sa.Integer(), nullable=True),
    sa.Column('profilePictureUrl', sa.Text(), nullable=True),
    sa.Column('biography', sa.Text(), nullable=True),
    sa.Column('website', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_AccountInfo_date'), 'AccountInfo', ['date'], unique=False)
    op.create_index(op.f('ix_AccountInfo_time'), 'AccountInfo', ['time'], unique=False)
    op.create_table('DailyFetch',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('time', sa.Time(), nullable=True),
    sa.Column('numFollowing', sa.Integer(), nullable=True),
    sa.Column('numFollowers', sa.Integer(), nullable=True),
    sa.Column('numPosts', sa.Integer(), nullable=True),
    sa.Column('numDailyVisits', sa.Integer(), nullable=True),
    sa.Column('numDailyFollowers', sa.Integer(), nullable=True),
    sa.Column('numDailyReach', sa.Integer(), nullable=True),
    sa.Column('numDailyImpressions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_DailyFetch_date'), 'DailyFetch', ['date'], unique=False)
    op.create_index(op.f('ix_DailyFetch_time'), 'DailyFetch', ['time'], unique=False)
    op.drop_index('ix_AutomatedDailyFetch_date', table_name='AutomatedDailyFetch')
    op.drop_index('ix_AutomatedDailyFetch_time', table_name='AutomatedDailyFetch')
    op.drop_table('AutomatedDailyFetch')
    op.drop_index('ix_DailyAccountInfoFetch_date', table_name='DailyAccountInfoFetch')
    op.drop_index('ix_DailyAccountInfoFetch_time', table_name='DailyAccountInfoFetch')
    op.drop_table('DailyAccountInfoFetch')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('DailyAccountInfoFetch',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"DailyAccountInfoFetch_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('numFollowing', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numFollowers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numPosts', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyVisits', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyFollowers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyReach', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyImpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('profilePictureUrl', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('biography', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('website', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='DailyAccountInfoFetch_pkey')
    )
    op.create_index('ix_DailyAccountInfoFetch_time', 'DailyAccountInfoFetch', ['time'], unique=False)
    op.create_index('ix_DailyAccountInfoFetch_date', 'DailyAccountInfoFetch', ['date'], unique=False)
    op.create_table('AutomatedDailyFetch',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"AutomatedDailyFetch_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('date', sa.DATE(), autoincrement=False, nullable=True),
    sa.Column('time', postgresql.TIME(), autoincrement=False, nullable=True),
    sa.Column('numFollowing', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numFollowers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numPosts', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyVisits', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyFollowers', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyReach', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('numDailyImpressions', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='AutomatedDailyFetch_pkey')
    )
    op.create_index('ix_AutomatedDailyFetch_time', 'AutomatedDailyFetch', ['time'], unique=False)
    op.create_index('ix_AutomatedDailyFetch_date', 'AutomatedDailyFetch', ['date'], unique=False)
    op.drop_index(op.f('ix_DailyFetch_time'), table_name='DailyFetch')
    op.drop_index(op.f('ix_DailyFetch_date'), table_name='DailyFetch')
    op.drop_table('DailyFetch')
    op.drop_index(op.f('ix_AccountInfo_time'), table_name='AccountInfo')
    op.drop_index(op.f('ix_AccountInfo_date'), table_name='AccountInfo')
    op.drop_table('AccountInfo')
    # ### end Alembic commands ###
