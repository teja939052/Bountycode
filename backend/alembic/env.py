import asyncio
from logging.config import fileConfig

from alembic import context
from app.config import get_settings
from app.database import get_engine
from app.models import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


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
    engine = get_engine()
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


async def run_migrations_offline():
    settings = get_settings()
    url = settings.SUPABASE_DB_URL or config.get_main_option("sqlalchemy.url")
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
