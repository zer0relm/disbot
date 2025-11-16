import sqlbot
import re

sql_connector = sqlbot.sqlBot()
test_word = "Sword"

ticks = sql_connector.getTicks()
for options in ticks:
    pass