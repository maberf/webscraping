# MAIN
from webtableparser import WebTableParser

site1 = WebTableParser()
site1.create('https://calculador.com.br/tabela/indice/IGP-M', 'table table-bordered table-striped table-hover table-fixed mb-0')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)

site2 = WebTableParser()
site2.create('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea', 'wikitable sortable')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)

site3 = WebTableParser()
site3.create('https://www.fundsexplorer.com.br/ranking', 'table table-hover')
table3 = site3.capture()
print(type(table3))
df3 = site3.parse(table3)
print(df3)
