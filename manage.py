#!/usr/bin/env python3
import json
import sqlite3
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

DB_PATH = "app.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


class Handler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload=None):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        if payload is not None:
            self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def _parse_book_id(self):
        path = urlparse(self.path).path
        parts = [p for p in path.split("/") if p]
        if len(parts) == 2 and parts[0] == "books":
            try:
                return int(parts[1])
            except ValueError:
                return None
        return None

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            return self._send_json(200, {"status": "ok"})

        if path == "/books":
            with get_conn() as conn:
                rows = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
            data = [dict(r) for r in rows]
            return self._send_json(200, {"data": data})

        book_id = self._parse_book_id()
        if book_id is not None:
            with get_conn() as conn:
                row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
            if row is None:
                return self._send_json(404, {"error": "Book not found"})
            return self._send_json(200, {"data": dict(row)})

        return self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/books":
            return self._send_json(404, {"error": "Not found"})

        body = self._read_json_body()
        if body is None:
            return self._send_json(400, {"error": "Invalid JSON"})

        title = body.get("title")
        author = body.get("author")
        year = body.get("year")

        if not title or not author:
            return self._send_json(400, {"error": "title and author are required"})
        if year is not None and not isinstance(year, int):
            return self._send_json(400, {"error": "year must be an integer"})

        now = datetime.utcnow().isoformat() + "Z"
        with get_conn() as conn:
            cur = conn.execute(
                """
                INSERT INTO books(title, author, year, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, author, year, now, now),
            )
            conn.commit()
            book_id = cur.lastrowid

            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

        return self._send_json(201, {"data": dict(row)})

    def do_PUT(self):
        book_id = self._parse_book_id()
        if book_id is None:
            return self._send_json(404, {"error": "Not found"})

        body = self._read_json_body()
        if body is None:
            return self._send_json(400, {"error": "Invalid JSON"})

        title = body.get("title")
        author = body.get("author")
        year = body.get("year")

        if not title or not author:
            return self._send_json(400, {"error": "title and author are required"})
        if year is not None and not isinstance(year, int):
            return self._send_json(400, {"error": "year must be an integer"})

        with get_conn() as conn:
            exists = conn.execute("SELECT id FROM books WHERE id = ?", (book_id,)).fetchone()
            if exists is None:
                return self._send_json(404, {"error": "Book not found"})

            now = datetime.utcnow().isoformat() + "Z"
            conn.execute(
                """
                UPDATE books
                SET title = ?, author = ?, year = ?, updated_at = ?
                WHERE id = ?
                """,
                (title, author, year, now, book_id),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

        return self._send_json(200, {"data": dict(row)})

    def do_DELETE(self):
        book_id = self._parse_book_id()
        if book_id is None:
            return self._send_json(404, {"error": "Not found"})

        with get_conn() as conn:
            exists = conn.execute("SELECT id FROM books WHERE id = ?", (book_id,)).fetchone()
            if exists is None:
                return self._send_json(404, {"error": "Book not found"})

            conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()

        return self._send_json(204)

    def log_message(self, format, *args):
        return


def runserver(host="0.0.0.0", port=8000):
    init_db()
    server = HTTPServer((host, port), Handler)
    display_host = "127.0.0.1" if host == "0.0.0.0" else host
    print(f"HTTP server running at http://{display_host}:{port}")
    print("Try: /health, /books")
    server.serve_forever()


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        host = sys.argv[2] if len(sys.argv) >= 3 else "0.0.0.0"
        port = int(sys.argv[3]) if len(sys.argv) >= 4 else 8000
        runserver(host=host, port=port)
    else:
        print("Usage: python manage.py runserver [host] [port]")


if __name__ == "__main__":
    main()
