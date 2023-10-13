from connection import cur


def insert_token(id_user, token, date_exp):
    cur.execute(f'''INSERT INTO token (id_user, token, expiration_date)
                VALUES("{id_user}", "{token}", "{date_exp}");''')
