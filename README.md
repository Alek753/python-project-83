### Hexlet tests and linter status:
[![Actions Status](https://github.com/Alek753/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Alek753/python-project-83/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/6082f2af7b2da90006be/maintainability)](https://codeclimate.com/github/Alek753/python-project-83/maintainability)
[![CI](https://github.com/Alek753/python-project-83/actions/workflows/lint_flake8.yml/badge.svg)](https://github.com/Alek753/python-project-83/actions/workflows/lint_flake8.yml)



# Проект 3: Анализатор страниц (Page Analyzer)
## Описание
Анализатор страниц (Page Analyzer) – это приложение на базе фреймворка Flask, которое анализирует заданные страницы на SEO-пригодность.

### [Приложение на Render.com](https://python-project-83-hvib.onrender.com)

## Системные требования
* Python 3.9
* Poetry 1.8.3
* PostgreSQL 12.20

## Установка

1. Клонировать репозиторий с GitHub:
   ```sh
   git clone https://github.com/Alek753/python-project-83
   ```

2. Создать роль в PosgreSQL с именем текущего пользователя:
   ```sh
   sudo -u postgres createuser --createdb <имя_текущего_пользователя>
   ```
   
4. Создать базу данных для работы приложения:
   ```sh
    sudo -u postgres createdb --owner=<имя_текущего_пользователя> <имя_базы_данных>
   ```  

5. Создать в корне директории проекта файл '.env' и заполнить его следующим образом:
   ```sh
   SECRET_KEY=ваш_секретный_ключ
   DATABASE_URL=postgresql://<имя_пользователя_из_шага_3>:пароль@localhost:5432/<имя_базы_данных_из_шага_3>
   ```

6. Запустить создание необходимых таблиц базы данных
   ```sh
   psql -f database.sql <имя_базы_данных_из_шага_3>
   ```

7. Запустить установку зависимостей, необходимых для запуска приложения:
   ```sh
   make install
   ```

8. Чтобы запустить приложение в режиме разработки (на flask):
   ```sh
   make dev
   ```

5. Чтобы запустить приложение в продакшене (на gunicorn):
   ```sh
   make start
   ```
