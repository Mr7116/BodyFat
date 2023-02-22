import pyodbc

class DataBase_Bodyfat:
    def __init__(self):
        self.conn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-VE11ESD\MSSQLSERVER2;DATABASE=bodyfat;')
        self.cursor = self.conn.cursor()

    def register(self, username, hashed_password):
        # self.cursor.execute('''INSERT INTO product (product_id, product_name, price) VALUES (5,'Chair',120), (6,'Tablet',300) ''')
        self.cursor.execute('INSERT INTO BFUSER (Username,Password) VALUES (?,?)',(username,hashed_password))      
        self.conn.commit()
        
        return self.cursor.rowcount
    def check_username(self,username):
        self.cursor.execute('SELECT * from BFUSER where ?  in (Username)',username)
        dt = {}
        for row in self.cursor.fetchall():
            dt["user_id"] = row[0]
            dt["username"] = row[1]
            dt["password"] = row[2]
        return dt

    def checktologin(self, username):
        # self.cursor.execute('''INSERT INTO product (product_id, product_name, price) VALUES (5,'Chair',120), (6,'Tablet',300) ''')
        self.cursor.execute('select * from BFUSER where Username = ?',username)      
        # self.conn.commit()
        dt = {}
        for row in self.cursor.fetchall():
            dt["user_id"] = row[0]
            dt["username"] = row[1]
            dt["password"] = row[2]
        return dt

