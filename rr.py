import psycopg2
import pandas as pd
import json

# Путь к файлу CSV
csv_file_path = "test_drinks.csv"

# Загрузка конфигурации базы данных
with open("db_config.json", "r", encoding="utf-8") as file:
    db_config = json.load(file)

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname=db_config["dbname"],
    user=db_config["user"],
    password=db_config["password"],
    host=db_config["host"],
    port=db_config["port"]
)
cur = conn.cursor()

# Читаем данные из CSV
file_path = "drinks_v2.csv"  # Укажите путь к файлу
df = pd.read_csv(file_path)

# SQL-запрос для вставки данных
insert_query = """
INSERT INTO drinks (
    category, description, ingredients, photo_url, notes,
    aroma_profile, taste_profile, sugar_content, producer,
    gastropair, name, subcategory
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Заполняем таблицу
for _, row in df.iterrows():
    cur.execute(insert_query, (
        row["category"], row["description"], row["ingredients"], row["photo_url"], row["notes"],
        row["aroma_profile"], row["taste_profile"], row["sugar_content"], row["producer"],
        row["gastropair"], row["name"], row["subcategory"]
    ))

# Сохраняем изменения и закрываем соединение
conn.commit()
cur.close()
conn.close()

