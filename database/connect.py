import pyodbc
import logging
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MSSQLConnection:
    def __init__(self, driver='SQL Server', server='QUANFX\QUANFX', 
                 database='BMI', username='', password=''):
        self.driver = driver
        self.server = server
        self.database = database
        self.username = username
        self.password = password

    def _connection_string(self):
        return (
            f'DRIVER={{{self.driver}}};'
            f'SERVER={self.server};'
            f'DATABASE={self.database};'
            f'UID={self.username};'
            f'PWD={self.password}'
        )

    @contextmanager
    def _get_connection(self):
        connection = None
        try:
            connection = pyodbc.connect(self._connection_string())
            logger.info('Connected to database')
            yield connection
        except pyodbc.Error as e:
            logger.error(f'Database connection error: {e}')
            raise
        finally:
            if connection:
                connection.close()
                logger.info('Connection closed')

    def query(self, sql, params=None):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                results = cursor.fetchall()
                logger.info(f'Query executed successfully: {sql}')
                return results
        except pyodbc.Error as e:
            logger.error(f'Error executing query: {e}')
            raise
    
    def query_one(self, sql, params=None):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                result = cursor.fetchone()
                logger.info(f'Query executed successfully: {sql}')
                return result
        except pyodbc.Error as e:
            logger.error(f'Error executing query: {e}')
            raise

    def execute(self, sql, params=None):
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params or ())
                conn.commit()
                logger.info(f'Statement executed and committed: {sql}')
        except pyodbc.Error as e:
            logger.error(f'Error executing statement: {e}')
            raise

    def insert(self, sql, params=None):
        self.execute(sql, params)

    def update(self, sql, params=None):
        self.execute(sql, params)

    def delete(self, sql, params=None):
        self.execute(sql, params)
