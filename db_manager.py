import psycopg2
import os


HOST = 'huggify-database-do-user-6412382-0.e.db.ondigitalocean.com'
DATABASE = 'defaultdb'
USER = 'doadmin'
PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
PORT = 25060

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
        is_premium BOOLEAN NOT NULL,
        birthday DATE NOT NULL,
        is_male BOOLEAN NOT NULL,
        premium_purchase_date TIMESTAMP NULL
    );
    ''')


@cur_wrapper
def create_images_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS images (
        id SERIAL PRIMARY KEY,
        FOREIGN KEY (user) REFERENCES users(id)
        score FLOAT NOT NULL,
        is_male BOOLEAN NOT NULL,
        url TEXT NOT NULL,
    );
    ''')


@cur_wrapper
def create_ratings_table(cur=None):
    cur.execute('''
    CREATE TABLE IF NOT EXISTS ratings (
        id SERIAL PRIMARY KEY,
        FOREIGN KEY (user) REFERENCES users(id)
        FOREIGN KEY (image1) REFERENCES images(id)
        FOREIGN KEY (image2) REFERENCES images(id)
        is_image1_voted BOOLEAN NOT NULL,
    );
    ''')


create_users_table()
create_images_table()
create_ratings_table()


@cur_wrapper
def create_new_user(is_premium: bool, uses: int, client_id: str, cur=None) -> None:
    a = 'TRUE' if is_premium else 'FALSE'
    cur.execute(f'''INSERT INTO users (, is_premium, premium_purchase_date) VALUES ('{client_id}', {a}, {uses}, NULL);''')


@cur_wrapper
def get_user_from_client_id(client_id: str, cur=None):
    cur.execute(f'''SELECT * FROM person WHERE client_id = '{client_id}';''')
    fetch = cur.fetchone()

    # If user doesn't exist, create one
    if not fetch:
        create_new_user(is_premium=False, uses=FREE_DEFAULT_USES, client_id=client_id)
        cur.execute(f'''SELECT * FROM person WHERE client_id = '{client_id}';''')
        fetch = cur.fetchone()
        user = fetch
        return user
    ###################################

    user = fetch
    return user


@cur_wrapper
def buy_monthly_with_client_id(client_id, cur=None):
    # Change is_premium = True to user
    cur.execute(f'''UPDATE person SET is_premium = TRUE, uses = {PREMIUM_DEFAULT_USES}, premium_purchase_date = NOW() WHERE client_id = '{client_id}';''')

    # Update all videos from the user and mark them as paid
    cur.execute(f'''UPDATE hugging_videos SET is_paid = TRUE WHERE client_id = '{client_id}';''')


@cur_wrapper
def buy_yearly_premium_with_client_id(client_id, cur=None):
    # Change is_premium = True to user
    cur.execute(f'''UPDATE person SET is_premium = TRUE, uses = {PREMIUM_DEFAULT_USES_YEARLY}, premium_purchase_date = NOW() WHERE client_id = '{client_id}';''')

    # Update all videos from the user and mark them as paid
    cur.execute(f'''UPDATE hugging_videos SET is_paid = TRUE WHERE client_id = '{client_id}';''')


@cur_wrapper
def cancel_premium_with_client_id(client_id, cur=None):
    cur.execute(f'''UPDATE person SET is_premium = FALSE, premium_purchase_date = NULL WHERE client_id = '{client_id}';''')


@cur_wrapper
def get_array_ratings_from_array_id(array, cur=None):
    query = '''SELECT * FROM hugging_videos WHERE id = ANY(%s) ORDER BY array_position(%s, id)'''
    cur.execute(query, (array, array))
    fetch = cur.fetchall()
    return fetch

