import os
from app.db.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from datetime import datetime
import mysql.connector
import json


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS domain_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(255) UNIQUE,
            da FLOAT,
            pa FLOAT,
            created_at VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS similarweb_stats (
            id INT AUTO_INCREMENT PRIMARY KEY,
            domain VARCHAR(255) UNIQUE,
            data TEXT,
            created_at VARCHAR(255)
        )
    """)
    conn.commit()
    conn.close()


def get_from_db(url: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT url, da, pa, created_at FROM domain_stats WHERE url = %s", (url,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return {"url": result[0], "da": result[1], "pa": result[2], "cached": True}
    return None


def save_to_db(url: str, da: float, pa: float):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO domain_stats (url, da, pa, created_at) VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE da=VALUES(da), pa=VALUES(pa), created_at=VALUES(created_at)
        """,
        (url, da, pa, now)
    )
    conn.commit()
    conn.close()


def get_similarweb_from_db(domain: str):
    """Get cached SimilarWeb data from database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT domain, data, created_at FROM similarweb_stats WHERE domain = %s", (domain,))
    result = cursor.fetchone()
    conn.close()
    if result:
        data = json.loads(result[1])
        return {"domain": result[0], "data": data, "cached": True, "cached_at": result[2]}
    return None


def save_similarweb_to_db(domain: str, data: dict):
    """Save SimilarWeb data to database"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO similarweb_stats (domain, data, created_at) VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE data=VALUES(data), created_at=VALUES(created_at)
        """,
        (domain, json.dumps(data), now)
    )
    conn.commit()
    conn.close()


def update_similarweb_in_db(domain: str, data: dict):
    """Update existing SimilarWeb data in database"""
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute(
        """
        UPDATE similarweb_stats 
        SET data = %s, created_at = %s 
        WHERE domain = %s
        """,
        (json.dumps(data), now, domain)
    )
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0



