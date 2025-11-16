import mysql.connector
import dotenv
import random

class sqlBot():
    def __init__(self):
        keys = dotenv.dotenv_values("test_db.env")
        self.mydb = mysql.connector.connect(
            host=keys["HOST"],
            user=keys["USER"],
            password=keys["PASSWORD"],
            database=keys["DATABASE"]
        )
        self.my_cursor = self.mydb.cursor(buffered=True)
        self.debug = False
        try:
            self.my_cursor.execute("SELECT * FROM quote_test")
        except mysql.connector.Error as error:
            print(error)

    def getRandomQuote(self):
        self.my_cursor.execute("SELECT count(*) FROM quote_test")
        quote_count = self.my_cursor.fetchone()
        random_quote_id = random.randint(1, quote_count[0])
        if self.debug:
            print(quote_count)
            print(random_quote_id)
        self.my_cursor.execute(f"SELECT * FROM quote_test WHERE quote_id = {random_quote_id}")
        quote = self.my_cursor.fetchone()
        return quote

    def addQuote(self, quote, user):
        sql = "INSERT INTO quote_test (quote_text, quoted_dttm, user) VALUES (%s, NOW(), %s)"
        values = (quote, user)
        self.my_cursor.execute(sql, values)
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM quote_test order by quote_id desc")
        return self.my_cursor.fetchone()

    def addUserTick(self, tick, user):
        sql = "INSERT INTO ticks (keyword, user) VALUES (%s, %s)"
        values = (tick, user)
        self.my_cursor.execute(sql, values)
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM ticks order by id desc")
        return self.my_cursor.fetchone()

    def addTick(self, tick: str):
        sql = "INSERT INTO ticks (keyword) VALUES (%s)"
        self.my_cursor.execute(sql, [tick])
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM ticks order by id desc")
        return self.my_cursor.fetchone()

    def getTicks(self):
        self.my_cursor.execute("SELECT * FROM ticks")
        ticks = self.my_cursor.fetchall()
        return ticks
