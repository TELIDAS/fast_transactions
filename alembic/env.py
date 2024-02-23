from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import Engine
from alembic import context
import asyncio
from dotenv import load_dotenv
import os

from db.models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

async_engine = create_async_engine(DATABASE_URL, echo=True)


def do_run_migrations(connection: Engine):
    """Run the migrations."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    async with async_engine.begin() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations():
    if context.is_offline_mode():
        raise NotImplementedError("Running migrations offline is not supported in this async setup.")
    else:
        asyncio.run(run_migrations_online())


run_migrations()
