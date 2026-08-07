"""
Terminal Pet Society - Persistence Layer
Saves and loads pet state using SQLite.
"""

import json
import os
import sqlite3
import time
from typing import Optional

from pet import Pet

DB_PATH = os.path.expanduser("~/.terminal-pet-society/pets.db")


def _ensure_db():
    """Ensure database and tables exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            name TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            updated_at REAL NOT NULL
        )
    """)
    # Settings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def save_pet(pet: Pet) -> bool:
    """Save pet state to database."""
    try:
        conn = _ensure_db()
        data = json.dumps(pet.to_dict())
        conn.execute(
            "INSERT OR REPLACE INTO pets (name, data, updated_at) VALUES (?, ?, ?)",
            (pet.name, data, time.time())
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving pet: {e}")
        return False


def load_pet(name: str) -> Optional[Pet]:
    """Load a pet by name."""
    try:
        conn = _ensure_db()
        row = conn.execute(
            "SELECT data FROM pets WHERE name = ?", (name,)
        ).fetchone()
        conn.close()
        if row:
            data = json.loads(row[0])
            return Pet.from_dict(data)
        return None
    except Exception as e:
        print(f"Error loading pet: {e}")
        return None


def list_saved_pets() -> list:
    """List all saved pet names."""
    try:
        conn = _ensure_db()
        rows = conn.execute(
            "SELECT name, updated_at FROM pets ORDER BY updated_at DESC"
        ).fetchall()
        conn.close()
        return [(r[0], r[1]) for r in rows]
    except Exception:
        return []


def delete_pet(name: str) -> bool:
    """Delete a pet."""
    try:
        conn = _ensure_db()
        conn.execute("DELETE FROM pets WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_setting(key: str, default: str = "") -> str:
    """Get a setting value."""
    try:
        conn = _ensure_db()
        row = conn.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        ).fetchone()
        conn.close()
        return row[0] if row else default
    except Exception:
        return default


def set_setting(key: str, value: str):
    """Set a setting value."""
    try:
        conn = _ensure_db()
        conn.execute(
            "INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)",
            (key, value)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass
