from postgres.psql import Database
from data_work import DataWork
from orders.export import DataExportDay
import time


def start():
    db = Database()
    db.delete()
    users = db.get_users()
    dt = DataWork().set_date()
    for user in users:
        exp = DataExportDay(dt, user[0])
        happy = exp.birthday()
        for j in happy:
            j.append(user[0])
            db.add_persons(user[0], j[0], j[1], j[2], dt)
        time.sleep(10)


if __name__ == '__main__':
    start()
