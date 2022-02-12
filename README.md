## Foodgram (yandex-practicum-project)
[![Foodgram workflow](https://github.com/H782705/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/H782705/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

Foodgram - онлайн сервис для публикации кулинарных рецептов. Пользователи могут создавать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное» и скачивать список продуктов для приготовления выбранных блюд.

Проект доступен по адресу: http://62.84.124.251/

Документация с описанием API endpoints проекта размещена [здесь](http://62.84.124.251/api/docs/)

### Установка и начало работы:
1. Установите Docker согласно [инструкции для вашей ОС](https://docs.docker.com/engine/install/). 
2. Склонируйте данный репозиторий: 
   ```
   git@github.com:h782705/foodgram-project-react.git
   ```
3. При необходимости измените настройки Django-приложения.   
  Создайте файл `.env` в корневой директории проекта и укажите в нем следующие переменные:
   * `DEBUG` - True/False для debug-режима
   * `ALLOWED_HOSTS`- список адресов по которым приложение принимает запросы. Для запуска на локальной машине укажите localhost;
  
4. Для работы с приложением используйте следующие команды в [директории infra](infra):
   * Запуск контейнеров: 
     ```
     docker-compose up -d --build
     ```
   * Создание миграций Django: 
     ```
     docker-compose exec infra_backend_1 python manage.py makemigrations
     ```
   * Применение миграций Django:  
     ```
     docker-compose exec infra_backend_1 python manage.py migrate
     ```
   * Создание суперюзера Django: 
     ```
     docker-compose exec infra_backend_1 python manage.py createsuperuser
     ```
   * Сборка статических файлов проекта: 
     ```
     docker-compose exec infra_backend_1 python manage.py collectstatic --no-input
     ``` 
   * Загрузка исходных данных из файла в БД (файл с данными есть в репозитории): 
     ```
     docker-compose exec infra_backend_1 python manage.py  load_ingredients < dump.json
     ```
   * Остановка контейнеров: 
     ```
     docker-compose down
     ```
