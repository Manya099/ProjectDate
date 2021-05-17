import sqlite3

# Проверяет, есть ли запись с таким id в базе данных
def is_user_exists(user_id):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXISTS(
            SELECT id 
            FROM users 
            WHERE id = ?
        )
    """, (user_id,))

    result = cursor.fetchone()[0]
    connection.close()

    if result == 0:
        return False
    else:
        return True


# Записывает пользователя в базу данных
def create_user(user_id, name, age, sex, partner_sex):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    try:
        if not is_user_exists(user_id):
            cursor.execute("""
                INSERT INTO users 
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, name, age, sex, partner_sex))

            connection.commit()
        else:
            print('Ошибка регистрации пользователя: пользователь с данным id уже зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("User creating error: " + str(error))
    else:
        connection.close()


# Обновляет данные пользователя по их имени
def update_userdata(user_id, data_name, data):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    try:
        if is_user_exists(user_id):
            cursor.execute("""
                UPDATE users 
                SET {} = ? 
                WHERE id = ?
            """.format(data_name), (data, user_id))

            connection.commit()
        else:
            print('Ошибка обновления данных: пользователь с данным id не зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("Updating error: " + error)
    else:
        connection.close()


# Получает данные пользовател по их имени
def read_userdata(user_id, data_name):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

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
    else:
        connection.close()


# Удаляет пользователя из базы данных
def delete_user(user_id):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    try:
        if is_user_exists(user_id):
            cursor.execute("""
                DELETE 
                FROM users 
                WHERE id = ?
            """, user_id)

            connection.commit()
        else:
            print('Ошибка удаления пользователя: пользователь с данным id не зарегистрирован')
    except sqlite3.DatabaseError as error:
        print("Deleting error: " + error)
    else:
        connection.close()


