# 🏢 B2B Platform for Booking (API)

Потужна B2B платформа для управління офісними просторами, кімнатами переговорів та робочими місцями. 
Проєкт розроблений як RESTful API для бізнесу, що дозволяє організаціям повністю ізольовано керувати своїми офісами, бронювати місця та отримувати детальну аналітику завантаженості.

## 🚀 Основні можливості (Features)

* **Multi-tenancy архітектура:** Кожна організація має власний ізольований простір. Користувачі взаємодіють лише з даними своєї компанії.
* **Гнучка ієрархія просторів:** Підтримка ланцюжка `Організація ➔ Офіс ➔ Кімната (Meeting/Open Space/Private) ➔ Робоче місце`.
* **Розумне бронювання:** Захист від подвійного бронювання (Overbooking) на рівні API.
* **Advanced Analytics:** Вбудований модуль аналітики, який автоматично вираховує відсоток завантаженості офісів за певний період, використовуючи оптимізовані SQL-агрегації.
* **Soft Delete:** Усі сутності підтримують м'яке видалення (`is_active=False`) для збереження фінансової та аналітичної історії.
* **Рольова модель:** Гнучке налаштування прав доступу (Користувач, Адміністратор організації, Staff-користувач системи).

## 🛠 Технологічний стек

* **Backend:** Python 3, Django, Django REST Framework (DRF)
* **Database:** PostgreSQL (рекомендовано) / SQLite (для розробки)
* **API Documentation:** drf-spectacular (OpenAPI 3 / Swagger)
* **Authentication:** JWT (JSON Web Tokens) або Session

## 📦 Встановлення та запуск (Локально)

1. **Клонуйте репозиторій:**
   ```bash
   git clone [https://github.com/kostantingolovenko/B2B-platform-for-booking.git](https://github.com/kostantingolovenko/B2B-platform-for-booking.git)
   cd B2B-platform-for-booking

2. **Створіть та активуйте віртуальне середовище:**
python -m venv .venv
source .venv/bin/activate  # Для Windows: .venv\Scripts\activate



3. **Встановіть залежності:**
```bash
pip install -r requirements.txt
```


4. **Застосуйте міграції:**
```bash
python manage.py migrate
```


5. **Створіть суперкористувача (Global Admin):**
```bash
python manage.py createsuperuser
```


6. **Запустіть локальний сервер:**
```bash
python manage.py runserver
```



## 📖 Документація API (Swagger)

Після запуску сервера, інтерактивна документація доступна за адресами:

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
* **OpenAPI Schema:** `http://127.0.0.1:8000/api/schema/`