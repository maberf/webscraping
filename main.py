# MAIN
# packages urllib, beatiful soup, html5, pandas
#
# from webtableparserpreviousversion import WebTableParser
from src.webtableparser import WebTableParser
#
# Sites 1 e 2 for testing (remove comments)
'''site1 = WebTableParser()
site1.create('https://calculador.com.br/tabela/indice/IGP-M',
             'table table-bordered table-striped table-hover table-fixed mb-0')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)'''
# Site by webtableparserpreviousversion module
'''site2 = WebTableParser('https://pt.wikipedia.org/wiki/\
    Lista_de_capitais_do_Brasil_por_%C3%A1rea',
                       'wikitable sortable')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)'''
# site capture and parsing
site = WebTableParser()
site.create('https://www.fundsexplorer.com.br/ranking',
            'table table-hover')
table = site.capture()
df = site.parse(table)
print(df)
#
# Now you have to process the dataframe, "clean and organize" it!
