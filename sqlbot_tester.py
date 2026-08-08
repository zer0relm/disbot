import sqlbot
import re

sql_connector = sqlbot.sqlBot()
test_word = "Sword"

keyword_list = sql_connector.getKeywords()
for keyword in keyword_list:
    print(keyword)