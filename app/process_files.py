import pandas as pd
import os
import re
from pathlib import Path
from io import BytesIO

from app.db import execute_query, insert_dataframe_to_db, table_exists_in_db


# Путь к папке с данными
data_directory = os.path.join('files')
# Путь к папке с файлами, которые нужно обработать
raw_files_directory = os.path.join(data_directory, 'raw_files')
# Путь к списку обработанных файлов
processed_files_list_path = os.path.join(raw_files_directory, 'processed_files.txt')
# Путь к папке с SQL-файлами
sql_files_directory = os.path.join(data_directory, 'sql_files')


def parse_file_overdue(file_name):
    # Названия столбцов
    columns_names = [
        'region_name',
        'medical_organization',
        'inn',
        'status',
        'withdrawal_from_circulation_type',
        'gtin',
        'series',
        'doses_per_pack_cnt',
        'packages_cnt',
        'doses_cnt',
        'expiration_date',
        'overdue_days'
    ]

    # Типы данных столбцов
    columns_types = {
        'region_name': str,
        'medical_organization': str,
        'inn': str,
        'status': str,
        'withdrawal_from_circulation_type': str,
        'gtin': str,
        'series': str,
        'doses_per_pack_cnt': int,
        'packages_cnt': int,
        'doses_cnt': int,
        'expiration_date': str,
        'overdue_days': int
    }

    # Сохраняем содержимое файла в датафрейм
    df = pd.read_excel(os.path.join(raw_files_directory, file_name), skiprows=4,
                       names=columns_names, dtype=columns_types)

    # Преобразуем поле "Срок годности" в дату
    df['expiration_date'] = pd.to_datetime(df['expiration_date'], format='%d.%m.%Y')

    return df


def upload_file_overdue_to_db(file_name):
    # Получаем список файлов, которые уже были загружены в базу данных
    with open(processed_files_list_path, 'r', encoding='utf-8') as f:
        processed_files = set(f.read().splitlines())

    # Если файл с таким названием есть в списке обработанных файлов - функция завершает работу
    if file_name in processed_files:
        return f'Файл "{file_name}" уже был ранее загружен в базу данных'

    # Схема и название таблицы, в которую будет загружен файл
    table_schema = 'public'
    table_name = 'overdue'

    # Проверяем, существует ли таблица в базе данных. Если нет - создаем ее
    if not table_exists_in_db(table_schema, table_name):
        # Получаем из SQL-файла запрос для создания таблицы
        with open(os.path.join(sql_files_directory, 'create_table_overdue.sql')) as f:
            query_to_create_table_overdue = f.read()

        # Запускаем запрос для создания таблицы
        execute_query(query_to_create_table_overdue)

    # Вызываем функцию, которая парсит Excel-файл и возвращает датафрейм
    df = parse_file_overdue(file_name)

    # Добавляем в датафрейм столбец "Дата актуальности данных" (дата берется из названия Excel-файла)
    pattern = re.compile(r'\((\d{2,}.\d{2,}.\d{4,})\)')
    date_from_file_name = pattern.search(file_name)
    if date_from_file_name:
        df['data_relevance_date'] = pd.to_datetime(date_from_file_name.group(1),
                                                   format='%d.%m.%Y',
                                                   errors='coerce')
    else:
        df['data_relevance_date'] = None

    # Загружаем датафрейм в таблицу базы данных
    insert_dataframe_to_db(df, table_schema, table_name)

    # Добавляем файл в список обработанных файлов
    with open(processed_files_list_path, 'a', encoding='utf-8') as f:
        f.write(f'{file_name}\n')

    return f'Файл "{file_name}" успешно загружен в базу данных'


def create_report_overdue(file_name):
    # Парсим файл и рассчитываем нужные метрики
    df = (
        parse_file_overdue(file_name)
        .groupby('region_name')
        .agg({
            'doses_cnt': 'sum',
            'overdue_days': 'mean'
        })
        .reset_index()
        .rename(columns={
            'region_name': 'Субъект РФ',
            'doses_cnt': 'Суммарное количество доз',
            'overdue_days': 'Среднее просрочено дней'
        })
    )
    df['Среднее просрочено дней'] = df['Среднее просрочено дней'].round()

    # Записываем датафрейм в объект BytesIO для отправки документа через Telegram-бота
    bio = BytesIO()
    bio.name = Path(file_name).stem + '_report.xlsx'
    df.to_excel(bio, index=False)
    bio.seek(0)

    return bio
