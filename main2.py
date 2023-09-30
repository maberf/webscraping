# MAIN
# packages urllib, beatiful soup, html5, pandas
#
from src.webtableparser2 import WebTableParser
#
# Site capture and parsing
'''site = WebTableParser()
site.create('https://www.fundsexplorer.com.br/ranking',
            'id', 'table-ranking')
table = site.capture()
df = site.parse(table)
print(df)'''