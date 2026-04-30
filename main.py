from app.database import init_db
from app.dashboard import Dashboard


def main():
    init_db()
    app = Dashboard()
    app.mainloop()


if __name__ == "__main__":
    main()