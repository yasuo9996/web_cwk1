#!/usr/bin/env python3
import sys


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "runserver":
        host = sys.argv[2] if len(sys.argv) >= 3 else "127.0.0.1"
        port = int(sys.argv[3]) if len(sys.argv) >= 4 else 8000
        uvicorn = __import__("uvicorn")
        uvicorn.run("app.main:app", host=host, port=port, reload=False)
    elif len(sys.argv) >= 2 and sys.argv[1] == "migrate":
        alembic = __import__("alembic.config", fromlist=["main"])
        alembic.main(argv=["-c", "alembic.ini", "upgrade", "head"])
    else:
        print("Usage: python manage.py runserver [host] [port]")
        print("   or: python manage.py migrate")


if __name__ == "__main__":
    main()
