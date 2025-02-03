CREATE TABLE public.overdue
(
    region_name VARCHAR,
    medical_organization VARCHAR,
    inn VARCHAR,
    status VARCHAR,
    withdrawal_from_circulation_type VARCHAR,
    gtin VARCHAR,
    series VARCHAR,
    doses_per_pack_cnt INTEGER,
    packages_cnt INTEGER,
    doses_cnt INTEGER,
    expiration_date DATE,
    overdue_days INTEGER,
    data_relevance_date DATE,
    data_upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE public.overdue IS 'Просроченные препараты';

COMMENT ON COLUMN public.overdue.region_name IS 'Субъект РФ';
COMMENT ON COLUMN public.overdue.medical_organization IS 'МО (медицинская организация)';
COMMENT ON COLUMN public.overdue.inn IS 'ИНН';
COMMENT ON COLUMN public.overdue.status IS 'Статус';
COMMENT ON COLUMN public.overdue.withdrawal_from_circulation_type IS 'Тип вывода из оборота';
COMMENT ON COLUMN public.overdue.gtin IS 'ГТИН';
COMMENT ON COLUMN public.overdue.series IS 'Серия';
COMMENT ON COLUMN public.overdue.doses_per_pack_cnt IS 'Дозы (количество доз в упаковке (флаконе))';
COMMENT ON COLUMN public.overdue.packages_cnt IS 'Количество Упаковок';
COMMENT ON COLUMN public.overdue.doses_cnt IS 'Количество Доз';
COMMENT ON COLUMN public.overdue.expiration_date IS 'Срок годности';
COMMENT ON COLUMN public.overdue.overdue_days IS 'Просрочено дней';
COMMENT ON COLUMN public.overdue.data_relevance_date IS 'Дата актуальности данных (берется из названия файла)';
COMMENT ON COLUMN public.overdue.data_upload_timestamp IS 'Дата и время загрузки данных в базу';