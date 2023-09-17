# MAIN
# packages urllib, beatiful soup, html5, pandas
#
from src.webtableparserprevious import WebTableParser
# from src.webtableparser import WebTableParser
#
# Site test for testing purposes by webtableparserprevious module. Change the import above.
# You can not use it, it´s only a previous version for testing of code essential.
sitetest = WebTableParser('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea',
                       'wikitable sortable')
tabletest = sitetest.capture()
dftest = sitetest.parse(tabletest)
print(dftest)
# Site capture and parsing
'''site = WebTableParser()
site.create('https://www.fundsexplorer.com.br/ranking',
            'id', 'table-ranking')
table = site.capture()
df = site.parse(table)
print(df)'''
#
# Now you have to process the dataframe, "clean and organize" it!
