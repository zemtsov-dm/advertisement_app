# API для сервиса по размещению объявлений.
Объявления могут быть разных видов (продажа, покупка, оказание услуг).
Основные роли системы: пользователь, администратор.

## Используемые технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)

## Основные возможности

Возможности пользователя:
 - Регистрация
 - Вход в систему
 - Размещение объявления
 - Просмотр списка объявлений 
 - Детальный просмотр одного объявления 
 - Удаление своего объявления
 - Размещение жалобы на объявление
						
Возможности администратора:
 - Все выше перечисленное
 - Удаление комментариев в любой группе объявлений 
 - Назначение пользователя администратором
 - Просмотр жалоб на объявлние
 - Перенос объявления из одной категории в другую
 - Бан/разбан пользователя администратором

Дополнитеьлные возможности:
 - Серверная пагинация
 - Фильтрация объявлений
 - Сортировка записей
 - Авторизация с помощью JWT-токена
 - Жалоба на объявление		
 - Настроен логгер для вывода в терминал и в Telegram



## Пример запроса:

Swagger схема доступна по [ссылке](https://github.com/zemtsov-dm/advertisement_app/blob/main/API%20Example%20-%20Swagger.mhtml) (скачать и открыть в браузере)

## Инструкция по запуску

1. Сначала клонируйте репозиторий

```
git clone https://github.com/zemtsov-dm/advertisement_app.git
```

2. Перейдите в каталог с проектом:

```
cd advertisement_app
```

3. Создайте файл .env и заполните необходимые переменные из файла .env_example своими данными

```
#Database settings
POSTGRES_USER=YOUR_PG_OUES # пример "postgres"
POSTGRES_PASSWORD=YOUR_PG_PASSWORD # пример "postgres"
POSTGRES_DB=YOUR_DB_NAME # пример "api_db"

DB_HOST="db" # не изменять
DB_PORT=5432 # не изменять

#JWT Settings
SECRET_KEY=YOUR_SECRET_KEY # можно сгенерировать через команду 'openssl rand -hex 32'
JWT_ALGORITHM='HS256' # не изменять
ACCESS_TOKEN_EXPIRE_MINUTES='60' # время жизни токена, можно установить желаемое

#Telegtam
CHAT_ID=YOUR_CHAT_ID # ваше id из telegram, можно получить у бота @getmyid_bot
BOT_TOKEN=YOUR_BOT_TOKEN # токен вашего бота, можно создать через @BotFather

#Logging level
API_LOG_LEVEL='INFO' # уровень логирования всего проекта
TELEGRAM_LOG_LEVEL='ERROR' #уровень логирования который уходит в бота телеграм
```

4. Выполните команду (убедитесь что у вас установлен Docker и Docker compose)

```
docker-compose up
```
5. Теперь ваш проект должен быть доступен по адресу http://localhost:8000/
   
6. Документация доступна по адресу http://localhost:8000/docs

