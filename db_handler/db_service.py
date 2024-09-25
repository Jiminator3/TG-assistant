from asyncpg_lite import DatabaseManager
from decouple import config
from sqlalchemy import Integer, String, TIMESTAMP

pg_manager = DatabaseManager(db_url=config('PG_LINK'), deletion_password=config('ROOT_PASS'))


async def create_table(table_name, new_columns: list):
    async with pg_manager:
        await pg_manager.create_table(table_name=table_name, columns=new_columns)
