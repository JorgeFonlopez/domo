import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def create_tables(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        # Define la sentencia SQL para crear la tabla users
        create_users_table_query = '''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        '''

        # Define la sentencia SQL para crear la tabla works
        create_works_table_query = '''
            CREATE TABLE IF NOT EXISTS works (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                work_name VARCHAR(255) NOT NULL,
                status VARCHAR(20) NOT NULL DEFAULT 'pendiente',
                registration_date DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        '''
      
        # Ejecuta las sentencias SQL para crear las tablas
        cursor.execute(create_users_table_query)
        
        cursor.execute(create_works_table_query)
        
        connection.commit()

        cursor.close()
        connection.close()
