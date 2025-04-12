import os
import pytds


def get_connection():
    server = os.getenv("DB_SERVER", "").strip()
    database = os.getenv("DB_NAME", "").strip()
    user = os.getenv("DB_USER", "").strip()
    password = os.getenv("DB_PASSWORD", "").strip()

    return pytds.connect(
        server=server,
        database=database,
        user=user,
        password=password,
        port=1433,
        timeout=15,
        validate_host=False,
        autocommit=True
    )
def get_models():
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ID, Titulo FROM Modelos")
            rows = cursor.fetchall()
            return [{"ID": row[0], "Titulo": row[1]} for row in rows]

def get_model_by_name(model_name):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT Titulo, Descripcion, referencia, urlImagen FROM modelos WHERE Titulo = %s",
                (model_name,)
            )
            row = cursor.fetchone()
            return {
                    "Titulo": row[0],
                    "Descripcion": row[1],
                    "referencia": row[2],
                    "urlImagen": row[3]
                }

