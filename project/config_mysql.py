from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from _login_mysql import HOST, USER, PASSWD, DB


def mysql_connection(host, user, passwd, database):
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}/{database}")
        connection = engine.connect()
    except OperationalError as e:
        if "Can't connect" in str(e):
            raise ValueError("Erro de conexão: Host incorreto.")
        elif "Unknown database" in str(e):
            raise ValueError("Erro de conexão: Nome do database incorreto.")
        else:
            raise Exception(f"Erro desconhecido: {str(e)}")
    except RuntimeError as e:
        if "sha256_password" or "caching_sha2_password" in str(e):
            raise ValueError("Erro de conexão: Usuário ou senha incorretos")
        else:
            raise Exception(f"Erro desconhecido: {str(e)}")
    else:
        print("Conexão realizada com sucesso")
        return connection

connection = mysql_connection(HOST, USER, PASSWD, DB)
