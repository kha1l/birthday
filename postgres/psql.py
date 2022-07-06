import psycopg2
from config.cfg import Settings
from datetime import date


class Database:
    @property
    def connection(self):
        stg = Settings()
        return psycopg2.connect(
            database=stg.dbase,
            user=stg.user,
            password=stg.password,
            host=stg.host,
            port='5432'
        )

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def get_data(self, name: str):
        sql = '''
            SELECT restId, restName, restUuid, userLogs, userPass, countryCode 
            FROM orders 
            WHERE restName=%s 
            order by restId
        '''
        parameters = (name,)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_users(self):
        sql = '''
            SELECT restName, restId, restTime
            FROM orders
            WHERE status=%s 
            order by restId
        '''
        parameters = ('work',)
        return self.execute(sql, parameters=parameters, fetchall=True)

    def add_persons(self, name_rest: str, person: str, post: str, age: str, dt: date):
        sql = '''
            INSERT INTO birthday (name_rest, person, post, age, date) 
            VALUES (%s, %s, %s, %s, %s)
        '''
        parameters = (name_rest, person, post, age, dt)
        self.execute(sql, parameters=parameters, commit=True)

    def delete(self):
        sql = '''
            delete from birthday
        '''
        self.execute(sql, commit=True)
