from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
from typing import List


class WebTableParser:

    def __init__(self, site, spdsheetClassName):
        """objetc to read spreadsheets in websites"""
        self.site = site
        self.spdsheetClassName = spdsheetClassName
        pass

    def capture(self):
        """Function to capture information in website
        Returns:
            [type]: [bs4.element.Tag]
        """
        # URL request through web browser agent
        siteurl = request.Request(self.site, headers={'User-Agent': 'Mozilla/5.0'})
        page = request.urlopen(siteurl)
        soup = BeautifulSoup(page, 'html5lib')
        table = soup.find('table', attrs={'class': self.spdsheetClassName})
        return table

    def parse(self, table):
        # assembling information to dataframe
        columns = 0
        lines = 0
        columnnames: List[str] = []
        #
        for row in table.find_all('tr'):  # 1o rastreamento (estrutura)
            # contar número de linhas e colunas
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                lines += 1
                if columns == 0:
                    columns = len(td_tags)
        #
            # captura o titulo das colunas - se tiver thead/th
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(columnnames) == 0:
                for th in th_tags:
                    columnnames.append(th.get_text())
        #
        # criando o dataframe com o pandas para armazenar os dados
        df = pd.DataFrame(columns=columnnames, index=range(0, lines))
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
        #
        return df
