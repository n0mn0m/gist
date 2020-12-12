"""
Example extended aioodbc configuration.
"""
import asyncio
import aioodbc
import pyodbc
from concurrent.futures import ThreadPoolExecutor

loop = asyncio.get_event_loop()

async def conn_attributes(conn):
    conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
    conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
    conn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')
    conn.setencoding(encoding='utf-8')

async def odbc_insert_worker(conn, val):
    async with conn.cursor() as cur:
        await cur.execute('insert into async_testing values (?)', val)
        await cur.commit()

async def db_main(loop, vals):
    dsn="foo"

    vals = list(vals)

    async with aioodbc.create_pool(dsn=dsn, loop=loop, executor=ThreadPoolExecutor(max_workers=3), after_created=conn_attributes) as pool:
        tasks = [do_insert(pool, val) for val in vals]
        await asyncio.gather(*tasks)

async def do_insert(pool, val):
    async with pool.acquire() as conn:
        await odbc_insert_worker(conn, val)

vals = range(0,1000)

loop.run_until_complete(db_main(loop, vals))
