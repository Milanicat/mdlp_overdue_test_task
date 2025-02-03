# mdlp_overdue_test_task

## Инструкция

1. Клонируйте репозиторий.
```
git clone https://github.com/Milanicat/mdlp_overdue_test_task
```

2. В файле `docker-compose.yml` замените плейсхолдер `YOUR_TOKEN` на токен бота.

**Пример:**

Исходный фрагмент файла `docker-compose.yml`:
```
telegram_bot:
    container_name: telegram_bot_container
    image: telegram_bot_image
    build: .
    volumes:
      - ./files:/~/mdlp_overdue_test_task/files
    environment:
      - BOT_TOKEN=YOUR_TOKEN
```

Фрагмент файла `docker-compose.yml` с подставленным токеном:
```
telegram_bot:
    container_name: telegram_bot_container
    image: telegram_bot_image
    build: .
    volumes:
      - ./files:/~/mdlp_overdue_test_task/files
    environment:
      - BOT_TOKEN=1234567890:abcdefg
```

3. Находясь внутри папки проекта, выполните команду:
```
docker-compose up -d
```

4. Убедитесь, что все контейнеры построены и работают.

5. Откройте бота https://t.me/mdlp_overdue_test_task_bot и нажмите "Старт".

6. Отправьте боту команду `/overdue_to_db`, чтобы загрузить файл "Просрочено (06.09.2022)" в базу данных.

7. Отправьте боту команду `/report`, чтобы получить файл с отчетом.


