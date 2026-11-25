"""SQLAlchemy declarative base for BountyCode PostgreSQL migration.

All domain models inherit from Base. Uses UUID primary keys with
server-generated UUIDs (gen_random_uuid()) via PostgreSQL extension.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import MetaData

# Naming convention for constraints and indexes
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)


class Base(DeclarativeBase):
    """Base declarative class with naming conventions."""

    metadata = metadata

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Generate tablename from class name (snake_case)."""
        import re

        name = cls.__name__
        # Insert underscore before capital letters (except first)
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
        return s2.lower()

    def __repr__(self) -> str:
        pk = self.__mapper__.primary_key[0].name
        pk_value = getattr(self, pk, None)
        return f"<{self.__class__.__name__}({pk}={pk_value})>"
