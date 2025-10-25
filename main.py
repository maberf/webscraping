# MAIN
# packages urllib, beatiful soup, html5, pandas
#
from src.webtableparser import WebTableParser
#
# Site capture and parsing
site = WebTableParser('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea',
                       'wikitable sortable')
table = site.capture()
df = site.parse(table)
print(df)