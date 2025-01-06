import pyodbc

class MSSQLConnection:
    def __init__(self, driver = 'SQL Server', server = 'QUANFX\QUANFX', database ='QLBH', username = '', password = ''):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password

        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}')
            print('Connected to database')

        except Exception as e:
            print('Error connecting to database:', e)   

    def query(self, sql):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print('Error querying:', e)

    def update(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print('Error updating:', e)

    def insert(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print('Error inserting:', e)

    def delete(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                self.connection.commit()
        except Exception as e:
            print('Error deleting:', e)
    
    def close(self):
        if self.connection:
            self.connection.close()
            print('Connection closed')

if __name__ == '__main__':
    conn = MSSQLConnection()
    conn.connect()
    rows = conn.query('SELECT * FROM KHACHHANG')
    for r in rows:
        print(r)

    conn.close()