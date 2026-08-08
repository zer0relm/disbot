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
        self.my_cursor.execute("SELECT count(*) FROM quote")
        quote_count = self.my_cursor.fetchone()
        random_quote_id = random.randint(1, quote_count[0])
        if self.debug:
            print(quote_count)
            print(random_quote_id)
        self.my_cursor.execute(f"SELECT * FROM quote WHERE quote_id = {random_quote_id}")
        quote = self.my_cursor.fetchone()
        return quote

    def addQuote(self, quote, user):
        sql = "INSERT INTO quote (quote_text, quoted_dttm, user) VALUES (%s, NOW(), %s)"
        values = (quote, user)
        self.my_cursor.execute(sql, values)
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM quote order by quote_id desc")
        return self.my_cursor.fetchone()

    def addUserKeyword(self, keyword, emoji, user):
        sql = "INSERT INTO keywords (word, emoji, user) VALUES (%s, %s, %s)"
        values = (keyword, emoji, user)
        self.my_cursor.execute(sql, values)
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM keywords order by kw_id desc")
        return self.my_cursor.fetchone()

    def addKeyword(self, keyword: str, emoji: str):
        sql = "INSERT INTO keywords (word, emoji) VALUES (%s, %s)"
        values = (keyword, emoji)
        self.my_cursor.execute(sql, values)
        self.mydb.commit()
        self.my_cursor.execute("SELECT * FROM keywords order by kw_id desc")
        return self.my_cursor.fetchone()

    def getKeywords(self):
        self.my_cursor.execute("SELECT * FROM keywords")
        ticks = self.my_cursor.fetchall()
        self.my_cursor.execute("SELECT count(*) FROM keywords")
        ticks_count = self.my_cursor.fetchone()
        return ticks
