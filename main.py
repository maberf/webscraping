# MAIN
# packages urllib, beatiful soup, html5, pandas
#
# from webtableparserpreviousversion import WebTableParser
from src.webtableparser import WebTableParser
#
# Sites 1 e 2 for testing (remove comments)
'''site1 = WebTableParser()
site1.create('https://calculador.com.br/tabela/indice/IGP-M', 'class',
             'table table-bordered table-striped table-hover table-fixed mb-0')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)'''
# Site 2 by webtableparserpreviousversion module.
# You can not use it, it´s only a previous version
'''site2 = WebTableParser('https://pt.wikipedia.org/wiki/\
    Lista_de_capitais_do_Brasil_por_%C3%A1rea',
                       'wikitable sortable')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)'''
# Site 3 capture and parsing
site = WebTableParser()
site.create('https://www.fundsexplorer.com.br/ranking',
            'id', 'table-ranking')
table = site.capture()
df = site.parse(table)
print(df)
#
# Now you have to process the dataframe, "clean and organize" it!
