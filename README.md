# Booking API

Система бронирования переговорных комнат.

## Требования
- Docker и Docker Compose

## Быстрый запуск

1. Создайте в корневой директории файл `.env` на основе ваших локальных данных (пример):
   ```env
   DB_USER=postgres
   DB_PASS=my_secret_password_123
   DB_PORT=5432
   DB_NAME=booking_db
   SECRET_KEY=super-secret-key-for-local-development-only
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30