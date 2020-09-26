from urllib import request
from bs4 import BeautifulSoup
import pandas as pd
from typing import List


class WebTableParser:
    """Class to extract and parse a website table
    The table should be exactly like titles in columns and data in lines
    Other kind of table can have miscfunction (or do not function)
    Args:
        site = url of the table
        tableClassName = the class tag of the table (search into \
            the HTML page source code using web browser)
    Instancing and functions (in this order in your main):
        1 - yoursite = WebTableParser()
        2 - yoursite.create('site', 'tableClassName')
        3 - yourtable = yoursite.capture()
        4 - yourdf = yoursite.parse(yourtable)
    Returns:
        [type] pandas.core.frame.DataFrame
    """
    site = ''
    tableClassName = ''

    @classmethod
    def create(cls, site, tableClassName):
        cls.site = site
        cls.tableClassName = tableClassName
        pass

    @classmethod
    def capture(cls):
        """Function captures information in website
        Returns:
            [type]: [bs4.element.Tag]
        """
        # URL request through web browser agent
        siteurl = request.Request(cls.site,
                                  headers={'User-Agent': 'Mozilla/5.0'})
        page = request.urlopen(siteurl)
        soup = BeautifulSoup(page, 'html5lib')
        table = soup.find('table', attrs={'class': cls.tableClassName})
        return table

    def parse(self, table):
        """Function extracts, parses and load table data into a pandas dataframe
        Args:
            table [type]: [bs4.element.Tag]
        Returns:
            [type]: [pandas.core.frame.DataFrame]
        """
        # assembling information to the dataframe
        columns = 0
        lines = 0
        columnnames: List[str] = []
        for row in table.find_all('tr'):  # 1st crawling (structure)
            # lines and columns conuting
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                lines += 1
                if columns == 0:
                    columns = len(td_tags)
            # columns title cpature - key th
            th_tags = row.find_all('th')
            if len(th_tags) > 0 and len(columnnames) == 0:
                for th in th_tags:
                    columnnames.append(th.get_text())
        # pandas dataframe creation to data storage
        df = pd.DataFrame(columns=columnnames, index=range(0, lines))
        row_marker = 0
        for row in table.find_all('tr'):  # 2nd crawling (dataframe load)
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker, column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
        #
        return df
