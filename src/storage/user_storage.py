from connection import cur


def select_user_by_token(token):
    cur.execute(f'SELECT a.* FROM user a INNER JOIN token b ON a.id = b.id WHERE b.token = "{token}"')


def insert_user(user, email, name, passwd, now):
    cur.execute(f'''INSERT INTO user (user, email, name, passwd, registration_date) 
        VALUES('{user}', '{email}', '{name}', '{passwd}', '{now}');''')


def select_passwd_id(user):
    cur.execute(f'SELECT passwd, id FROM user WHERE user = "{user}"')


def select_all_users():
    cur.execute("SELECT * FROM user;")
