import sqlite3, random

class UserIDError(Exception):
    pass

class DatabaseError(Exception):
    pass

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
    """, (str(user_id),))

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

    if not is_user_exists(user_id):
        try:
            cursor.execute("""
                INSERT INTO users 
                VALUES (?, ?, ?, ?, ?)
            """, (str(user_id), str(name), str(age), str(sex), str(partner_sex)))

            connection.commit()
        except Exception as error:
            raise DatabaseError(str(error))
        else:
            connection.close()
    else:
        raise UserIDError('User with id ' + str(user_id + ' alredy exists'))
        connection.close


# Обновляет данные пользователя по их имени
def update_userdata(user_id, data_name, data):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    if is_user_exists(user_id):
        try:
            cursor.execute("""
                UPDATE users 
                SET {} = ?                 
                WHERE id = ?
            """.format(str(data_name)), (str(data), str(user_id)))

            connection.commit()
        except Exception as error:
            raise DatabaseError(str(error))
        else:
            connection.close()
    else:
        raise UserIDError('User with id ' + str(user_id + ' not exists'))
        connection.close()


# Получает данные пользовател по их имени
def read_userdata(user_id, data_name):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    if is_user_exists(user_id):
        try:
            cursor.execute("""
                SELECT {} 
                FROM users 
                WHERE id = ?
            """.format(str(data_name)), (str(user_id),))

            return cursor.fetchone()[0]
        except Exception as error:
            raise DatabaseError(str(error))
        else:
            connection.close()
    else:
        raise UserIDError('User with id ' + str(user_id + ' not exists'))
        connection.close()


#Загружает фотографию пользователя в базу данных
def get_image(user_id):
    pass


#Получает фотографию пользователя из базы данных
def set_image(user_id, image):
    image_data = bytearray(image.read())
    update_userdata(user_id, 'image', image_data)


# Удаляет пользователя из базы данных
def delete_user(user_id):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    if is_user_exists(user_id):
        try:
            cursor.execute("""
                DELETE 
                FROM users 
                WHERE id = ?
            """, (str(user_id),))

            connection.commit()
        except Exception as error:
            raise DatabaseError(str(error))
        else:
            connection.close()
    else:
        raise UserIDError('User with id ' + str(user_id + ' not exists'))
        connection.close()


# Возвращает id пользователя, подходящего под критерии отбора пользователя с id user_id
def get_partner(user_id):
    connection = sqlite3.connect("database.sqlite")
    cursor = connection.cursor()

    sex = read_userdata(user_id, 'sex')
    partner_sex = read_userdata(user_id, 'partner_sex')

    if is_user_exists(user_id):
        try:
            if partner_sex == 'any':
                cursor.execute("""
                    SELECT id
                    FROM users
                    WHERE partner_sex = ? OR partner_sex = "any
                """, (str(sex),))
            else:
                cursor.execute("""
                    SELECT id
                    FROM users
                    WHERE sex = ? AND (partner_sex = ? OR partner_sex = "any)
                """, (str(partner_sex), str(sex)))

            partners = cursor.fetchall()
            partner_id = partners[random.randint(len(partners))]

            return partner_id
        except Exception as error:
            raise DatabaseError(str(error))
        else:
            connection.close()
    else:
        raise UserIDError('User with id ' + str(user_id + ' not exists'))
        connection.close