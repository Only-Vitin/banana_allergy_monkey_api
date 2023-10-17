from connection import cur


def select_user_by_token(token):
    cur.execute(f'SELECT u.* FROM user u INNER JOIN token t ON u.id = t.id WHERE t.token = "{token}"')

def insert_user(user, email, name, passwd, now):
    cur.execute(f'''INSERT INTO user (user, email, name, passwd, registration_date) 
        VALUES('{user}', '{email}', '{name}', '{passwd}', '{now}');''')

def select_passwd_id(user):
    cur.execute(f'SELECT passwd, id FROM user WHERE user = "{user}"')

def select_all_users():
    cur.execute("SELECT * FROM user;")

def update_register_by_token(token, user, name, email, passwd, now):
    cur.execute(f'''UPDATE user SET user = '{user}', name = '{name}', email = '{email}', passwd = '{passwd}', registration_date = '{now}' WHERE user.id = (SELECT id_user FROM token WHERE token = '{token}')''')