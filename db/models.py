from sqlalchemy import (
    Column, ForeignKey, Integer,
    MetaData, String, Table,
    DateTime, func)
from sqlalchemy.ext.declarative import declarative_base, as_declarative


def all_column_names(constraint, table):
    try:
        return '_'.join([
            column.name for column in constraint.columns.values()
        ])
    except AttributeError as error:
        pass


convention = {
    'all_column_names': all_column_names,
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}


@as_declarative(metadata=MetaData(naming_convention=convention))
class Base:
    id = Column('id', Integer, primary_key=True)

    def __repr__(self):
        return f"<{self.__name__}(id='{self.id}')>"


# https://www.compose.com/articles/schema-migrations-with-alembic-python-and-postgresql/
# https://habr.com/ru/company/yandex/blog/511892/

class Comment(Base):
    __tablename__ = 'comments'

    board_id = Column('board_id', String(36), nullable=False, index=True)
    content = Column('content', String(255), nullable=False)
    user_name = Column('user_name', String(255), nullable=True)
    parent_id = Column('parent_id', Integer, ForeignKey('comments.id'), nullable=True)
    created = Column('created', DateTime(timezone=True), server_default=func.now())
    updated = Column('updated', DateTime(timezone=True), onupdate=func.now())
