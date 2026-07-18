import sqlite3
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "appointments.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            service TEXT NOT NULL,
            master TEXT NOT NULL,
            date_time TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_appointment(user_id: int, username: Optional[str], service: str, master: str, date_time: str):
    conn = get_connection()
    conn.execute(
        "INSERT INTO appointments (user_id, username, service, master, date_time) VALUES (?, ?, ?, ?, ?)",
        (user_id, username, service, master, date_time),
    )
    conn.commit()
    conn.close()


def is_slot_available(service: str, master: str, date_time: str) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT 1 FROM appointments WHERE service = ? AND master = ? AND date_time = ?",
        (service, master, date_time),
    ).fetchone()
    conn.close()
    return row is None


def get_user_appointments(user_id: int) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT service, master, date_time, created_at FROM appointments WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_all_users() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT user_id, username FROM appointments"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_today_appointments_count() -> int:
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(*) FROM appointments WHERE date(created_at) = date('now')"
    ).fetchone()[0]
    conn.close()
    return count


def get_total_users_count() -> int:
    conn = get_connection()
    count = conn.execute(
        "SELECT COUNT(DISTINCT user_id) FROM appointments"
    ).fetchone()[0]
    conn.close()
    return count
