import mysql.connector

# Настройки подключения к MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',              # если не задавал пароль в phpMyAdmin
    'database': 'your_db_name'   # замени на свою базу
}

# Подключение к базе данных
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# Получить список продуктов
def get_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM products")
    products = cursor.fetchall()
    conn.close()
    return products


# Добавить продукт
def add_product(name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (%s, %s)", (name, price))
    conn.commit()
    conn.close()


# Изменить продукт
def edit_product(product_id, name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = %s, price = %s WHERE id = %s", (name, price, product_id))
    conn.commit()
    conn.close()


# Удалить продукт
def delete_product(product_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    conn.commit()
    conn.close()
