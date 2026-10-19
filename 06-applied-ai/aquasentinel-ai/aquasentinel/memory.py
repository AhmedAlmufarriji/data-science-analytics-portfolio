"""Small transparent SQLite session memory. No hidden third-party data sharing."""
from __future__ import annotations

import sqlite3
from pathlib import Path


class SessionMemory:
    def __init__(self, path: str = ":memory:") -> None:
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, "
                          "session_id TEXT NOT NULL, role TEXT NOT NULL, "
                          "content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS preferences (session_id TEXT PRIMARY KEY, "
                          "district TEXT NOT NULL)")
        self.conn.commit()

    def remember(self, session_id: str, role: str, content: str) -> None:
        if role not in ("user", "assistant"):
            raise ValueError("Invalid message role")
        self.conn.execute("INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)",
                          (session_id, role, content[:600]))
        self.conn.commit()

    def recent(self, session_id: str, limit: int = 5) -> list[dict]:
        rows = self.conn.execute("SELECT role, content FROM messages WHERE session_id=? "
                                 "ORDER BY id DESC LIMIT ?", (session_id, min(20, max(1, limit)))).fetchall()
        return [{"role": role, "content": content} for role, content in reversed(rows)]

    def set_district(self, session_id: str, district: str) -> None:
        if district not in ("North", "Central", "East"):
            raise ValueError("Invalid district")
        self.conn.execute("INSERT INTO preferences (session_id, district) VALUES (?, ?) "
                          "ON CONFLICT(session_id) DO UPDATE SET district=excluded.district",
                          (session_id, district))
        self.conn.commit()

    def district(self, session_id: str) -> str | None:
        row = self.conn.execute("SELECT district FROM preferences WHERE session_id=?", (session_id,)).fetchone()
        return row[0] if row else None

    def clear(self, session_id: str) -> None:
        self.conn.execute("DELETE FROM messages WHERE session_id=?", (session_id,))
        self.conn.execute("DELETE FROM preferences WHERE session_id=?", (session_id,))
        self.conn.commit()
