import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "bot_data.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Uyarılar tablosu
    c.execute("""
        CREATE TABLE IF NOT EXISTS warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Banlı kullanıcılar tablosu (kayıt amaçlı)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            reason TEXT,
            banned_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# --- UYARI FONKSİYONLARI ---

def add_warning(chat_id: int, user_id: int, reason: str = None) -> int:
    """Uyarı ekle, toplam uyarı sayısını döndür."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO warnings (chat_id, user_id, reason) VALUES (?, ?, ?)",
        (chat_id, user_id, reason)
    )
    conn.commit()
    c.execute(
        "SELECT COUNT(*) as cnt FROM warnings WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    count = c.fetchone()["cnt"]
    conn.close()
    return count


def remove_warning(chat_id: int, user_id: int) -> int:
    """Son uyarıyı kaldır, kalan uyarı sayısını döndür."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT id FROM warnings WHERE chat_id=? AND user_id=? ORDER BY id DESC LIMIT 1",
        (chat_id, user_id)
    )
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM warnings WHERE id=?", (row["id"],))
        conn.commit()
    c.execute(
        "SELECT COUNT(*) as cnt FROM warnings WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    count = c.fetchone()["cnt"]
    conn.close()
    return count


def get_warnings(chat_id: int, user_id: int):
    """Kullanıcının tüm uyarılarını getir."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM warnings WHERE chat_id=? AND user_id=? ORDER BY created_at DESC",
        (chat_id, user_id)
    )
    rows = c.fetchall()
    conn.close()
    return rows


def clear_warnings(chat_id: int, user_id: int):
    """Tüm uyarıları temizle."""
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "DELETE FROM warnings WHERE chat_id=? AND user_id=?",
        (chat_id, user_id)
    )
    conn.commit()
    conn.close()


# --- BAN KAYIT FONKSİYONLARI ---

def log_ban(chat_id: int, user_id: int, reason: str = None, banned_by: int = None):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO bans (chat_id, user_id, reason, banned_by) VALUES (?, ?, ?, ?)",
        (chat_id, user_id, reason, banned_by)
    )
    conn.commit()
    conn.close()
