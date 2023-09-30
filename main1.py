# MAIN
# packages urllib, beatiful soup, html5, pandas
#
from src.webtableparser1 import WebTableParser
#
# Site capture and parsing
sitetest = WebTableParser('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea',
                       'wikitable sortable')
tabletest = sitetest.capture()
dftest = sitetest.parse(tabletest)
print(dftest)
