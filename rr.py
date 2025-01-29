import psycopg2
import json
import pandas as pd

# Загружаем конфиг подключения к БД
with open("db_config.json", "r", encoding="utf-8") as file:
    db_config = json.load(file)

# Путь к файлу CSV
file_path = "test_menu.csv"


def create_connection():
    """Создает и возвращает соединение с базой данных PostgreSQL."""
    return psycopg2.connect(
        dbname=db_config["dbname"],
        user=db_config["user"],
        password=db_config["password"],
        host=db_config["host"],
        port=db_config["port"]
    )


def create_table():
    """Создает таблицу в PostgreSQL, если она не существует."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS faq (
        id SERIAL PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        explanation TEXT
    );
    """

    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
        print("Таблица 'faq' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании таблицы: {e}")


def insert_data():
    """Заполняет таблицу данными из CSV."""
    df = pd.read_csv(file_path)

    # Если в файле нет id, PostgreSQL сам сгенерирует его
    insert_query = """
    INSERT INTO faq (question, answer, explanation)
    VALUES (%s, %s, %s)
    ON CONFLICT DO NOTHING;
    """

    try:
        conn = create_connection()
        with conn:
            with conn.cursor() as cur:
                for _, row in df.iterrows():
                    cur.execute(insert_query, (row["question"], row["answer"], row.get("explanation", None)))
        print("Данные успешно загружены в базу данных.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")


if __name__ == "__main__":
    create_table()
    insert_data()
