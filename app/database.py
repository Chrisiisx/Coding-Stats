import sqlite3
from datetime import datetime

DB_NAME = "codingstats.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            process TEXT NOT NULL,
            title TEXT,
            category TEXT,
            started_at TEXT NOT NULL,
            ended_at TEXT NOT NULL,
            duration_seconds INTEGER NOT NULL
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_app_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            process TEXT NOT NULL,
            category TEXT NOT NULL,
            total_seconds INTEGER NOT NULL DEFAULT 0,
            UNIQUE(date, process, category)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_language_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            language TEXT NOT NULL,
            total_seconds INTEGER NOT NULL DEFAULT 0,
            UNIQUE(date, language)
        )
    """)
    
    conn.commit()
    conn.close()


def save_session(process, title, category, started_at, ended_at):
    duration = int((ended_at - started_at).total_seconds())

    if duration <= 0:
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO activity_sessions 
        (process, title, category, started_at, ended_at, duration_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        process,
        title,
        category,
        started_at.isoformat(),
        ended_at.isoformat(),
        duration
    ))

    conn.commit()
    conn.close()
    
def update_daily_stats(process, category, started_at, ended_at):
    duration = int((ended_at - started_at).total_seconds())

    if duration <= 0:
        return

    date = started_at.date().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_app_stats (date, process, category, total_seconds)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(date, process, category)
        DO UPDATE SET total_seconds = total_seconds + excluded.total_seconds
    """, (
        date,
        process,
        category,
        duration
    ))

    conn.commit()
    conn.close()
    
def add_bulk_seconds_to_daily_stats(stats):
    if not stats:
        return

    from datetime import date
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for (process, category), seconds in stats.items():
        cursor.execute("""
            INSERT INTO daily_app_stats (date, process, category, total_seconds)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(date, process, category)
            DO UPDATE SET total_seconds = total_seconds + excluded.total_seconds
        """, (
            today,
            process,
            category,
            seconds
        ))

    conn.commit()
    conn.close()
    
def add_bulk_seconds_to_daily_language_stats(stats):
    if not stats:
        return

    from datetime import date
    today = date.today().isoformat()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for language, seconds in stats.items():
        cursor.execute("""
            INSERT INTO daily_language_stats (date, language, total_seconds)
            VALUES (?, ?, ?)
            ON CONFLICT(date, language)
            DO UPDATE SET total_seconds = total_seconds + excluded.total_seconds
        """, (
            today,
            language,
            seconds
        ))

    conn.commit()
    conn.close()