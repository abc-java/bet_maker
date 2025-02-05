
1. **Конфигурация:**
    В файле конфигурации необходимо заполнить следующие переменные:
    DB_URI=postgresql+asyncpg://postgres:postgres@postgres_db:5432
    DB_NAME=line_provider
    ECHO_SQL=False
    BET_MAKER_URL=http://127.0.0.1:8000 - адрес микросервиса bet_maker

    Можно создавать несколько файлов с конфигурацией и с помощью
    переменной окружения APP_CONFIG_FILE выбирать необходимую

    Файл конфигурации должен быть назван по шаблону <str>.env, где
    str имя файла, которое указывается в переменной APP_CONFIG_FILE для выбора 
    нужной конфигурации

    Что бы выбрать конфигурацию по умолчанию:
    ```bash
   export APP_CONFIG_FILE=local
   ```


1. **Для запуска добавьте в etc_hosts:**
    ```bash
    echo "127.0.0.1 postgres_db" | sudo tee -a /etc/hosts
    ```


1. **Поднимите Docker с помощью команды:**
   ```bash
   docker compose up
   ```
   

1. **Запуск без докера:**
   ```bash
   poetry run alembic upgrade head 
   poetry run python3 -m app
   ```

