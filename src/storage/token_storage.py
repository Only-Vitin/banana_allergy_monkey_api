from connection import cur


def select_token_by_user(user):
    cur.execute(
        f"""SELECT t.token FROM token t INNER JOIN user u ON u.id = t.id_user
        WHERE u.user = "{user}";"""
    )


def insert_token(id_user, token, date_exp):
    cur.execute(
        f"""INSERT INTO token (id_user, token, expiration_date)
        VALUES("{id_user}", "{token}", "{date_exp}");"""
    )


def delete_token(token):
    cur.execute(f'DELETE FROM token WHERE token = "{token}";')


def search_token(token):
    cur.execute(f'SELECT * FROM token WHERE token = "{token}";')
