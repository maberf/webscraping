# MAIN
from webtableparser import WebTableParser
from fundsexplorer import processFE_df
# import pandas as pd
# import numpy as np
# from matplotlib import pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
#
'''Sites for testing

site1 = WebTableParser()
site1.create('https://calculador.com.br/tabela/indice/IGP-M',
            'table table-bordered table-striped table-hover table-fixed mb-0')
table1 = site1.capture()
df1 = site1.parse(table1)
print(df1)

site2 = WebTableParser()
site2.create('https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea',
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
#
# real state fund varible, df processing to make analysis feasible (filters)
rsf = processFE_df(df)
# dataframe to real state funds (rsf) being filtered
rsf = rsf.loc[rsf['dy12macum%'] >= 4.00]  # 1st filter DY > 4%
rsf = rsf.loc[rsf['patrliqR$'] >= 500000000.00]  # 2nd filter > BRL 500 M
rsf = rsf.loc[rsf['liqdiariaNeg'] >= 1000]  # 3rd filter tradings >= 1000/day
rsf = rsf.loc[rsf['p/vpaN'] <= 1.25]  # 4th filter P/VPA <= 1.25
# Splitting into two new variables: brick and paper funds
rsf_brick = rsf.loc[rsf['qtdativosN'] >= 10]  # 5th filter >= 10 assets
rsf_paper = rsf.loc[rsf['qtdativosN'] == 0]  # 5 th filter = 0 assets
#
# pd.options.plotting.backend="plotly"
py.init_notebook_mode(connected=True)
#
# BAR CHARTS - YOU SHOULD TO COMMENT ONE TO GET ANOTHER
# bar chart 1 - brick funds
x0 = [rsf_brick['setor'], rsf_brick['codigo']]
trace00 = go.Bar(x=x0, y=rsf_brick['dy12macum%'],
                 name='DY% Ano', marker_color='rgb(36, 124, 220)')
trace01 = go.Bar(x=x0, y=rsf_brick['p/vpaN'],
                 name='P/VPA', marker_color='rgb(85, 171, 124)')
trace02 = go.Bar(x=x0, y=rsf_brick['vacfisica%'],
                 name='%Vacância Física', marker_color='rgb(213, 83, 43)')
data0 = [trace00, trace01, trace02]
fig0 = go.Figure(data0)
fig0.update_layout(title='ANÁLISE FIIs TIJOLOS | DY Ano >= 4%, Patr. > 500M, \
    Neg/dia > 1000, P/VPA =< 1.25, Ativos >= 10, Vacância Física < 15%')
fig0.show()
py.plot(fig0)
# bar chart 2 - paper funds
x1 = [rsf_paper['setor'], rsf_paper['codigo']]
trace10 = go.Bar(x=x1, y=rsf_paper['dy12macum%'], name='DY% Ano',
                 marker_color='rgb(36, 124, 220)')
trace11 = go.Bar(x=x1, y=rsf_paper['p/vpaN'], name='P/VPA',
                 marker_color='rgb(85, 171, 124)')
trace12 = go.Bar(x=x1, y=rsf_paper['varpatr%'], name='%Var. Patr. Acum',
                 marker_color='rgb(213, 83, 43)')
data1 = [trace10, trace11, trace12]
fig1 = go.Figure(data1)
fig1.update_layout(title='ANÁLISE FIIs PAPEL | DY Ano >= 4%, Patr. > 500M, \
    Neg/dia > 1000, P/VPA =< 1.25')
fig1.show()
py.plot(fig1)
