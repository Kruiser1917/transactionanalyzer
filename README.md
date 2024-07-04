# Анализатор транзакций

Этот проект представляет собой приложение для анализа транзакций из Excel-файла. Приложение генерирует JSON-данные для веб-страниц, формирует Excel-отчеты и предоставляет различные сервисы.

## Структура проекта

Проект имеет следующую структуру:

├── src
│ ├── init.py
│ ├── utils.py
│ ├── main.py
│ ├── views.py
│ ├── reports.py
│ └── services.py
├── data
│ └── operations.xlsx
├── tests
│ ├── init.py
│ ├── test_utils.py
│ ├── test_views.py
│ ├── test_reports.py
│ └── test_services.py
├── .flake8
├── .gitignore
├── pyproject.toml
├── poetry.lock
└── README.md


## Установка

1. Клонируйте репозиторий и перейдите в каталог проекта:
    ```sh
    git clone <репозиторий>
    cd <проектный каталог>
    ```

2. Создайте виртуальное окружение и активируйте его:
    ```sh
    python -m venv .venv
    .venv\\Scripts\\activate  # Windows
    source .venv/bin/activate  # Unix-подобные системы
    ```

3. Установите зависимости с помощью `poetry`:
    ```sh
    poetry install
    ```

## Запуск

Для запуска анализа транзакций выполните команду:

```sh
python src/main.py --file data/operations.xlsx --action <действие>
```

Где <действие> может быть одним из следующих:

main_page
events_page
expenses_by_category
expenses_by_day_of_week
expenses_by_workday_weekend
expenses_by_hour
analyze_cashback
analyze_investment
simple_search
phone_number_search
individual_transfers_search
Примеры:

python src/main.py --file data/operations.xlsx --action main_page
python src/main.py --file data/operations.xlsx --action events_page
python src/main.py --file data/operations.xlsx --action expenses_by_category --year 2021 --month 12

Тестирование
Для запуска тестов используйте pytest:
pytest tests/

Конфигурация
Файл .flake8 для настройки проверки PEP8:

[flake8]
max-line-length = 119
exclude = .git,__pycache__,.venv

Файл pyproject.toml для настройки black и isort:

[tool.black]
line-length = 119
exclude = '''
/(
    \.git
  | \.venv
)/
'''

[tool.isort]
line_length = 119

[tool.black]
line-length = 119
exclude = '''
/(
    \.git
  | \.venv
)/
'''

Примечания
Все ключи для авторизации в API скрыты в файле .env.
В репозитории есть шаблон файла .env_template с указанием всех необходимых переменных.


### Инструкции по созданию файла:

1. Откройте ваш текстовый редактор (например, VS Code, Notepad++, или обычный блокнот).
2. Создайте новый файл.
3. Скопируйте приведенный выше текст и вставьте его в новый файл.
4. Сохраните файл с именем `README.md` в корневом каталоге вашего проекта.



