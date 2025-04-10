import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")


def cur_wrapper(func):
    def wrapper(*args, **kwargs):
        con = psycopg2.connect(host=HOST, database=DBNAME, user=USER, password=PASSWORD, port=PORT)
        cur = con.cursor()
        print('Im in')
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
        client_id TEXT NOT NULL,
        birthday DATE NOT NULL,
        is_male BOOLEAN NOT NULL,
        email TEXT DEFAULT '',
        is_premium BOOLEAN DEFAULT false,
        premium_purchase_time TIMESTAMP NULL,
        created_at TIMESTAMPTZ DEFAULT now()
    );
    ''')


@cur_wrapper
def create_images_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,
        score FLOAT DEFAULT 1200,
        is_male BOOLEAN NOT NULL,
        url TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        created_at TIMESTAMPTZ DEFAULT now()
    );
    ''')


@cur_wrapper
def create_ratings_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        image1_id INT NOT NULL,
        image2_id INT NOT NULL,
        is_image1_voted BOOLEAN NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now(),
        FOREIGN KEY (image1_id) REFERENCES images(id),
        FOREIGN KEY (image2_id) REFERENCES images(id)
    );
    ''')


create_users_table()
create_images_table()
create_ratings_table()


@cur_wrapper
def get_user_from_client_id(client_id: str, birthday: str, is_male: bool, cur=None):
    cur.execute(f'''SELECT * FROM users WHERE client_id = '{client_id}';''')
    user = cur.fetchone()

    # If user doesn't exist, create one
    if not user:
        cur.execute(f'''
            INSERT INTO users (client_id, birthday, is_male)
            VALUES ('{client_id}', '{birthday}', {is_male})
            RETURNING *;
        ''')
        user = cur.fetchone()
        return user
    ###################################

    # (id, client_id, birthday, is_male, email, is_premium, premium_purchase_date, created_at)
    return user


@cur_wrapper
def create_new_image_record(user_id: int, is_male: bool, img_format: str = '.jpg', cur=None) -> tuple:
    cur.execute(f'''
    INSERT INTO images (is_male, url, user_id)
    VALUES (
    {is_male},
    (concat('user_images/{user_id}/', currval('images_id_seq')::text, '{img_format}')),
    {user_id}
    )
    RETURNING *;
    ''')
    image = cur.fetchone()
    # (id, user_id, score, is_male, is_male, url, created_at)
    return image


@cur_wrapper
def buy_monthly_premium_with_client_id(client_id, cur=None):
    cur.execute(f'''UPDATE users SET is_premium = TRUE, premium_purchase_time = NOW() WHERE client_id = '{client_id}';''')


@cur_wrapper
def cancel_premium_with_client_id(client_id, cur=None):
    cur.execute(f'''UPDATE users SET is_premium = FALSE, premium_purchase_time = NULL WHERE client_id = '{client_id}';''')
