import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from app.config import get_settings
from app.database import get_engine, get_session_factory

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = None


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=False,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    settings = get_settings()
    engine = get_engine()
    async with engine.connect() as connection:
        await connection.run_sync(lambda conn: context.configure(
            connection=conn,
            target_metadata=target_metadata,
            compare_type=True,
            include_schemas=False,
        ))
        await connection.run_sync(lambda conn: context.run_migrations())
    logger.info("PostgreSQL migrations completed successfully")


async def run_migrations_offline():
    settings = get_settings()
    url = settings.SUPABASE_DB_URL or "postgresql+asyncpg://postgres:postgres@localhost:5432/bountycode"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    asyncio.run(run_migrations_offline())
else:
    asyncio.run(run_migrations_online())