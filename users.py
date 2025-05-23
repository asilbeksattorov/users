"""users nomli tabelga Pythonda User classi yozasiz va ushbu
classda save(),get_users, get_user,delete_user(),update_user() metodlari
bo'lsin va bu metod ishlaganda bazadayam o'zgarishlar hosil bo'lsin
"""
import psycopg2
from typing import Optional

conn = psycopg2.connect(database = 'homework3',
                        user = 'postgres',
                        host = 'localhost',
                        password = '0909',
                        port = '5432')

cursor = conn.cursor()

"""
create_users_table_query = '''create table if not exists users (
                         id serial primary key,
                         full_name varchar(255) not null,
                         password varchar(255) not null,
                         email varchar(255) not null

);
'''

cursor.execute(create_users_table_query)
conn.commit()
"""


class User:

    def __init__(self, full_name : str,
                 password : Optional[str] = None,
                 email : Optional[str] = None):

        self.full_name = full_name
        self.password = password
        self.email = email


    def save(self):
        insert_into_query = '''
        insert into users (full_name, password, email)
        values (%s, %s, %s);
        '''

        data = (self.full_name, self.password, self.email)
        cursor.execute(insert_into_query, data)
        conn.commit()



    @classmethod
    def get_users(cls) -> List['User']:
        select_query = '''
        SELECT *
        FROM users;
        '''

        cursor.execute(select_query)
        rows = cursor.fetchall()
        users = [cls(full_name=row[0], password=row[1], email=row[2]) for row in rows]
        return users

    @classmethod
    def get_user(cls, user_id: int) -> Optional['User']:
        select_query = '''
        SELECT *
        FROM users
        WHERE id = %s;
        '''

        cursor.execute(select_query, (user_id,))
        row = cursor.fetchone()
        if row:
            return cls(full_name=row[0], password=row[1], email=row[2])
        else:
            return None

    def delete(self):
        delete_query = '''
        DELETE FROM users
        WHERE id = %s;
        '''

        cursor.execute(delete_query, (self.id,))
        conn.commit()

    def update(self, full_name: Optional[str] = None,
               password: Optional[str] = None,
               email: Optional[str] = None):
        update_query = '''
        UPDATE users
        SET full_name = (%s, full_name),
            password = (%s, password),
            email = (%s, email)
        WHERE id = %s;
        '''

        data = (full_name, password, email, self.id)
        cursor.execute(update_query, data)
        conn.commit()


john = User('John Doe', 'john123', 'johndoe@gmail.com')
john.save()

