import psycopg2
import os


HOST = '127.0.0.1'
DATABASE = 'postgres'
USER = 'postgres'
PASSWORD = 'toor'
PORT = 5432

FREE_DEFAULT_USES = 3
PREMIUM_DEFAULT_USES = 10
PREMIUM_DEFAULT_USES_YEARLY = 100


def cur_wrapper(func):
    def wrapper(*args, **kwargs):
        con = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD, port=PORT)
        cur = con.cursor()
        kwargs['cur'] = cur
        result = func(*args, **kwargs)
        con.commit()
        cur.close()
        con.close()
        return result
    return wrapper


@cur_wrapper
def create_users_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        is_premium BOOLEAN DEFAULT false,
        birthday DATE DEFAULT NULL,
        is_male BOOLEAN NOT NULL,
        email TEXT DEFAULT '',
        premium_purchase_date TIMESTAMP NULL
    );
    ''')


@cur_wrapper
def create_images_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        score FLOAT DEFAULT 1000,
        is_male BOOLEAN NOT NULL,
        url TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')


@cur_wrapper
def create_ratings_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        image1_id INT NOT NULL,
        image2_id INT NOT NULL,
        is_image1_voted BOOLEAN NOT NULL
        
    );
    ''')


create_users_table()
create_images_table()
create_ratings_table()


@cur_wrapper
def create_new_user_and_get_user(birthday: str, is_male: bool, cur=None) -> int:
    cur.execute(f'''
    INSERT INTO users (birthday, is_male) 
    VALUES ('{birthday}', {is_male})
    RETURNING id;;
    ''')
    db_user_id = cur.fetchone()[0]
    return db_user_id


@cur_wrapper
def create_new_image_record(user_id: int, is_male: bool, cur=None) -> None:
    cur.execute(f'''
    INSERT INTO images (is_male, url, user_id) 
    VALUES ({is_male},
    (concat('user_images/{user_id}/', currval('images_id_seq')::text, '.jpg')),
    {user_id});
    ''')
