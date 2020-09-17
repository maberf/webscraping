# MAIN
from webtableparser import WebTableParser

site1 = WebTableParser('https://www.fundsexplorer.com.br/ranking', 'table-ranking')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)
# id='table-ranking' class='table table-hover'

site2 = WebTableParser('http://www.idealsoftwares.com.br/indices/igp_m.html', 'tabA')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)
#site2.parse(table2)
# https://calculador.com.br/tabela/indice/IGP-M
# class="tabelaValoresIndice table-striped table table-bordered table-hover mb-0"
