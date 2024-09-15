# Flask-сервер с Celery для работы с данными

Этот проект представляет собой Flask-сервер, который использует Celery для выполнения задач по сохранению данных в базу данных и конвертации данных из формата JSON в XML и наоборот.

## Запуск сервера

Для запуска сервера используйте команду:

```bash 
docker-compose up -d --build
```
## Управление базой данных
### Пересоздание базы данных
Для пересоздания базы данных используйте команду:
```bash 
docker-compose exec web python manage.py create_db
```

### Получение элемента базы данных по ID
Чтобы получить элемент базы данных сущности EntrantChoice, используйте команду:
```bash 
docker-compose exec web python manage.py all_db_id_1 {id}
```
где {id} — это ID сущности EntrantChoice в базе данных.

### Просмотр списка всех сущностей EntrantChoice
Чтобы посмотреть список всех сущностей EntrantChoice, используйте команду:
docker-compose exec web python manage.py all_db

## Описание сущностей

### EntrantChoice

Сущность `EntrantChoice` имеет следующие поля:
- `json_data` — данные в формате JSON.
- `xml_data` — данные в формате XML.
- Ссылка на сущность `AddEntrant`.

### AddEntrant

Сущность `AddEntrant` содержит:
- `snils` — СНИЛС.
- `id_gender` — ID пола.
- `birthday` — Дата рождения.
- `birthplace` — Место рождения.
- `phone` — Телефон.
- `email` — Электронная почта.
- `id_oksm` — ID ОКСМ.

Она также связана с сущностью `AddressList`, которая включает:
- Список адресов (`addresses`), состоящий из:
  - `id` — ID адреса.
  - `full_addr` — Полный адрес.
  - `city` — Город.
  - `is_registration` — Является ли адрес регистрационным.
  - `id_region` — ID региона.


