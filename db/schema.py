from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, String, Table,
    DateTime, func)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}

metadata = MetaData(naming_convention=convention)
# https://www.compose.com/articles/schema-migrations-with-alembic-python-and-postgresql/
# https://habr.com/ru/company/yandex/blog/511892/
comments_table = Table(
    'comments',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('boardId', String(36), nullable=False, index=True),
    Column('content', String(255), nullable=False),
    Column('user_name', String(255), nullable=True),
    Column('parent_id', Integer, ForeignKey('comments.id'), nullable=True),
    Column('created', DateTime(timezone=True), server_default=func.now()),
    Column('updated', DateTime(timezone=True), onupdate=func.now())
)
