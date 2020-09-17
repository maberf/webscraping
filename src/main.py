# MAIN
from webtableparser import WebTableParser

site1 = WebTableParser('https://www.fundsexplorer.com.br/ranking', 'table table-hover')
table1 = site1.capture()
print(type(table1))
df1 = site1.parse(table1)
print(df1)
# id='table-ranking' class='table table-hover'''

'''site2 = WebTableParser('https://calculador.com.br/tabela/indice/IGP-M', 'table table-bordered table-striped table-hover table-fixed mb-0')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)'''

'''site3 = WebTableParser('https://sidra.ibge.gov.br/home/ipca/brasil', 'quadro tabela-sidra')
table3 = site3.capture()
print(table3)
df3 = site3.parse(table3)
print(df3)
# class = 'quadro tabela-sidra'  id = ipca-q1'''

site4 = WebTableParser('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea', 'wikitable sortable')
table4 = site4.capture()
df4 = site4.parse(table4)
print(df4)
