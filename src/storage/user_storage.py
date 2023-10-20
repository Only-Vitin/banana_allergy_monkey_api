from connection import cur


def select_user_by_token(token):
    cur.execute(f'SELECT u.* FROM user u INNER JOIN token t ON u.id = t.id_user WHERE t.token = "{token}"')

def select_id_by_token(token):
    cur.execute(f'SELECT id_user FROM token WHERE token = "{token}"')

def select_passwd_id(user):
    cur.execute(f'SELECT passwd, id FROM user WHERE user = "{user}";')

def search_user(user):
    cur.execute(f'SELECT * FROM user WHERE user = "{user}"')

def search_email(email):
    cur.execute(f'SELECT * FROM user WHERE email = "{email}"')

def select_all_users():
    cur.execute("SELECT * FROM user;")

def insert_user(user, email, name, passwd, now):
    cur.execute(f'''INSERT INTO user (user, email, name, passwd, registration_date) 
        VALUES('{user}', '{email}', '{name}', '{passwd}', '{now}');''')

def update_register_by_token(token, user, name, email, passwd, now):
    cur.execute(f'''UPDATE user SET user = '{user}', name = '{name}', email = '{email}', passwd = '{passwd}', registration_date = '{now}' WHERE user.id = (SELECT id_user FROM token WHERE token = '{token}');''')

def delete_register_by_id(id):
    cur.execute(f'''DELETE FROM token WHERE id_user = "{id}";''')
    cur.execute(f'''DELETE FROM user WHERE id = "{id}";''')