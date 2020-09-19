# MAIN
from webtableparser import WebTableParser
# import numpy
# import re

'''site1 = WebTableParser()
site1.create('https://calculador.com.br/tabela/indice/IGP-M', 'table table-bordered table-striped table-hover table-fixed mb-0')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)

site2 = WebTableParser()
site2.create('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea', 'wikitable sortable')
table2 = site2.capture()
df2 = site2.parse(table2)
print(df2)'''

site = WebTableParser()
site.create('https://www.fundsexplorer.com.br/ranking', 'table table-hover')
table = site.capture()
df = site.parse(table)

# Dataframe manipulation
df.columns = ['codigo', 'setor', 'precoatualR$', 'liqdiariaNeg', 'dividR$', 'divyield%', 'dy3macum%', 'dy6macum%', 'dy12macum%', 'dy3mmedia%', 'dy6mmedia%', 'dy12mmedia%', 'dyano%',  'varpreco%', 'rentper%', 'rentacum%', 'patrliqR$', 'vpaR$', 'p/vpaN', 'dypatr%', 'varpatr%', 'rentpatrper%', 'rentpatracum%', 'vacfisica%', 'vacfinan%', 'qtdativosN']
df = df.applymap(lambda x: str(x).replace('R$', ''))
df = df.applymap(lambda x: str(x).replace('%', ''))
df['precoatualR$'] = df['precoatualR$'].apply(lambda x: str(x).replace('.', ''))
df['patrliqR$'] = df['patrliqR$'].apply(lambda x: str(x).replace('.', ''))
df['vpaR$'] = df['vpaR$'].apply(lambda x: str(x).replace('.', ''))
df = df.applymap(lambda x: str(x).replace(',', '.'))
df['setor'] = df['setor'].apply(lambda x: str(x).replace('Ã', 'i'))
# df['setor'] = df['setor'].apply(lambda x: re.sub(r'Ã ', 'i', x))
df['setor'] = df['setor'].astype('string')
# df['precoatualR$'] = df['precoatualR$'].astype('float64')
# df['liqdiariaNeg'] = df['liqdiariaNeg'].astype('int64')
# print(df['setor'])
# print(type(df['setor']))
print(df)
print(df.info())
