import pandas as pd
from sqlalchemy import create_engine, text

from app import POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


engine = create_engine(f'postgresql://'
                       f'{POSTGRES_USER}:'
                       f'{POSTGRES_PASSWORD}@'
                       f'{POSTGRES_HOST}:{POSTGRES_PORT}/'
                       f'{POSTGRES_DB}')


def execute_query(query):
    with engine.connect() as db_conn:
        db_conn.execute(text(query))
        db_conn.commit()


def insert_dataframe_to_db(df, table_schema, table_name):
    with engine.connect() as db_conn:
        df.to_sql(
            con=db_conn,
            schema=table_schema,
            name=table_name,
            if_exists='append',
            index=False
        )
        db_conn.commit()


def table_exists_in_db(table_schema, table_name):
    with engine.connect() as db_conn:
        table_exists = pd.read_sql_query('SELECT to_regclass(%(table)s) IS NOT NULL AS table_exists',
                                         db_conn,
                                         params={'table': f'{table_schema}.{table_name}'})
    return table_exists.iloc[0]['table_exists']
