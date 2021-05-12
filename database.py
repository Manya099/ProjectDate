import sqlite3

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()


# Проверяет, есть ли запись с таким id в базе данных
def is_user_exists(user_id):
    cursor.execute("""
        SELECT EXISTS(
            SELECT id 
            FROM users 
            WHERE id = ?
        )
    """, user_id)

    result = cursor.fetchone()[0]

    if result == '0':
        return False
    else:
        return True


# Записывает пользователя в базу данных
def create_user(user_id, name, age, sex, partner_sex):
    try:
        if not is_user_exists(user_id):
            cursor.execute("""
                INSERT INTO users 
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, age, sex, partner_sex))
        else:
            print('Ошибка регистрации пользователя: пользователь с данным id уже зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("User creating error: " + error)
    else:
        connection.commit()


# Обновляет данные пользователя по их имени
def update_userdata(user_id, data_name, data):
    try:
        if is_user_exists(user_id):
            cursor.execute("""
                UPDATE users 
                SET {} = ? 
                WHERE id = ?
            """.format(data_name), (data, user_id))
        else:
            print('Ошибка обновления данных: пользователь с данным id не зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("Updating error: " + error)
    else:
        connection.commit()


# Получает данные пользовател по их имени
def read_userdata(user_id, data_name):
    try:
        if is_user_exists(user_id):
            cursor.execute("""
                SELECT {} 
                FROM users 
                WHERE id = ?
            """.format(data_name), user_id)

            return cursor.fetchone()[0]
        else:
            print('Ошибка чтения данных: пользователь с данным id не зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("Reading error: " + error)


# Удаляет пользователя из базы данных
def delete_user(user_id):
    try:
        if is_user_exists(user_id):
            cursor.execute("""
                DELETE 
                FROM users 
                WHERE id = ?
            """, user_id)
        else:
            print('Ошибка удаления пользователя: пользователь с данным id не зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("Deleting error: " + error)
    else:
        connection.commit()


