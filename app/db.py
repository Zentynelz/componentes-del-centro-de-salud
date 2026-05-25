import mysql.connector
import pandas as pd
from mysql.connector import Error
from config import DB_CONFIG


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        raise RuntimeError(f"Error al conectar con MySQL: {e}") from e


def fetch_dataframe(query: str, params: tuple = ()) -> pd.DataFrame:
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    finally:
        conn.close()


def fetch_options(query: str, params: tuple = ()) -> list:
    conn = get_connection()
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    finally:
        if cursor:
            cursor.close()
        conn.close()


def test_connection() -> bool:
    conn = get_connection()
    try:
        return conn.is_connected()
    finally:
        conn.close()
