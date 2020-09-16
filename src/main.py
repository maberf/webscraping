from urllib import request
from bs4 import BeautifulSoup
import pandas as pd

# URL request com agente de navegador
site = request.Request('https://www.fundsexplorer.com.br/ranking',
                       headers={'User-Agent': 'Mozilla/5.0'})
page = request.urlopen(site)
# print(page.read())#OK?
soup = BeautifulSoup(page, 'html5lib')
all_table = soup.find_all('table')
table = soup.find('table', class_='table table-hover')
# print(table.find_all('tr')) #Ok?

# PARSER

# atributos da estrutura do dataframe
nColunas = 0
nLinhas = 0
column_names = []

for row in table.find_all('tr'):  # 1o rastreamento (informações da estrutura)

    # contar número de linhas e colunas
    td_tags = row.find_all('td')
    if nColunas == 0:
        nColunas = len(td_tags)
    if len(td_tags) > 0:
        nLinhas += 1

    # captura o titulo das colunas - se tiver thead/th
    th_tags = row.find_all('th')
    if len(th_tags) > 0 and len(column_names) == 0:
        for th in th_tags:
            column_names.append(th.get_text())

# print(nLinhas, nColunas, column_names) #OK?

# criando o dataframe com o pandas para armazenar os dados
df = pd.DataFrame(columns=column_names, index=range(0, nLinhas))
row_marker = 0

# percorre as celulas para extrair o texto e gravar no dataframe
for row in table.find_all('tr'):  # 2o rastreamento (carregamento df)
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        df.iat[row_marker, column_marker] = column.get_text()
        column_marker += 1
    if len(columns) > 0:
        row_marker += 1

print(df)
