from os import environ
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from exceptions import UnknownError


load_dotenv()


def mysql_connection(host, user, passwd, database):
    try:
        engine = create_engine(f"mysql+pymysql://{user}:{passwd}@{host}/{database}")
        connection = engine.connect()
    except OperationalError as e:
        if "Can't connect" in str(e):
            raise ValueError("Erro de conexão: Host incorreto.") from e
        if "Unknown database" in str(e):
            raise ValueError("Erro de conexão: Nome do database incorreto.") from e
        raise UnknownError(f"Erro desconhecido: {str(e)}") from e
    except RuntimeError as e:
        if "sha256_password" in str(e) or "caching_sha2_password" in str(e):
            raise ValueError("Erro de conexão: Usuário ou senha incorretos") from e
        raise UnknownError(f"Erro desconhecido: {str(e)}") from e
    print("Conexão realizada com sucesso")
    return connection


conn = mysql_connection(
    environ["HOST"], environ["USER"], environ["PASSWD"], environ["DB"]
)

cur = conn.connection.cursor()
