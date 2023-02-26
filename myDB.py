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

    def insert_history(self, username:str, bmi:float ,bmi_text:str,fat_percen:float,body_fat:float,user_id):
        # self.cursor.execute('''INSERT INTO product (product_id, product_name, price) VALUES (5,'Chair',120), (6,'Tablet',300) ''')
        print(username, bmi ,bmi_text,fat_percen,body_fat,user_id)
        self.cursor.execute('INSERT INTO HISTORY (USERNAME,BMI,BMI_TEXT,FAT_PERCENTAGE,BODY_FAT,User_ID) VALUES (?,?,?,?,?,?)',(username,float(bmi),bmi_text,float(fat_percen),float(body_fat),user_id))      
        self.conn.commit()
        
        return self.cursor.rowcount

    def FindHistory(self, user_id):
        # self.cursor.execute('''INSERT INTO product (product_id, product_name, price) VALUES (5,'Chair',120), (6,'Tablet',300) ''')
        self.cursor.execute('select * from HISTORY where User_ID = ?',user_id)      
        # self.conn.commit()
        dtt = self.cursor.fetchall()
        list_dt = []
        i = 1
        for row in self.cursor.fetchall():
            dt = {}
            dt["num_count"] = i
            dt["username"] = row[1]
            dt["bmi"] = row[2]
            dt["bmi_text"] = row[3]
            dt["fat_percen"] = row[4]
            dt["body_fat"] = row[5]
            list_dt.append(dt)
            i += 1
        return dtt