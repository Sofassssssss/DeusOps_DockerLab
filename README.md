# DeusOps_DockerLab
## Лабораторная работа Docker: докеризация приложения
#### Вовченко София 2384

---

В качестве приложения для развертывания был взят старый проект одногруппника с его разрешения. Приложение является простым мессенджером с доской объявлений.
Изначально БД являлась SQLite, была переписана на PostgreSQL.

БД - PostgreSQL

Backend – Flask

Был написан Dockerfile:
```dockerfile
FROM python:3.10-alpine
LABEL authors="sofiavovchenko"

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN mkdir -p /app/static /app/templates

CMD alembic upgrade head && python main.py


```

Используется легковесный образ Python 3.12 на базе Alpine. Миграции перед запуском проводятся с помощью alembic. 
Так как в проекте используются статические записи, в Dockerfile создается 2 папки для хранения статики и шаблонов в контейнере.

Далее был написан docker-compose.yml:
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: sofiavovchenko
      POSTGRES_PASSWORD: Wmi_1234
      POSTGRES_DB: webby
    ports:
      - "5433:5432"
    healthcheck:
      test: pg_isready -U $$POSTGRES_USER -d $$POSTGRES_DB
      interval: 5s
      timeout: 3s
      retries: 5

  web:
    build: .
    volumes:
      - ./static:/app/static
      - ./templates:/app/templates
    environment:
      DB_URL: postgresql+psycopg2://sofiavovchenko:Wmi_1234@db:5432/webby
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
```

В качестве образа для БД используется легковесный образ PostgreSQL15 на базе Alpine.
Также с хоста был проброшен порт 5433 на 5432 порт контейнера для возможности сообщения между ними. 
Для healthcheck используется команда pg_isready для текущего пользователя и БД. 

В сервисе сервера определены volumes, чтобы работать с данными, которые хранятся за пределами его файловой системы. 
С помощью них монтируются директории с хоста внутрь контейнера(в данном случае это необходимо сделать, так как в проекте присутствуют статические данные).
Также определен environment для DB_URL и проброшен порт 8080 на 8080.
В depends_on написано от чего зависит этот сервис, в частности он не запустится пока db не пройдет healthcheck. 

В качестве проверки можно зайти на localhost:8080 и посмотреть приложение.
