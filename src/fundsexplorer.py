import pandas as pd
# import re


def processFE_df(df):
    """Function to process Pandas dataframe from Funds Explorer site:
    'https://www.fundsexplorer.com.br/ranking'
    After this function the DataFrame can be filtered to analysis
    Args:
        df ([type]): pandas.core.frame.DataFrame
    Returns:
        [type]: pandas.core.frame.DataFrame
    """
    df.columns = ['codigo', 'setor', 'precoatualR$', 'liqdiariaNeg',
                  'dividR$', 'divyield%', 'dy3macum%', 'dy6macum%',
                  'dy12macum%', 'dy3mmedia%', 'dy6mmedia%', 'dy12mmedia%',
                  'dyano%', 'varpreco%', 'rentper%', 'rentacum%',
                  'patrliqR$', 'vpaR$', 'p/vpaN', 'dypatr%', 'varpatr%',
                  'rentpatrper%', 'rentpatracum%', 'vacfisica%',
                  'vacfinan%', 'qtdativosN']
    df = df.applymap(lambda x: str(x).replace('R$', ''))
    df = df.applymap(lambda x: str(x).replace('%', ''))
    df['precoatualR$'] = df['precoatualR$'].apply(lambda x:
                                                  str(x).replace('.', ''))
    df['patrliqR$'] = df['patrliqR$'].apply(lambda x:
                                            str(x).replace('.', ''))
    df['vpaR$'] = df['vpaR$'].apply(lambda x: str(x).replace('.', ''))
    df = df.applymap(lambda x: str(x).replace(',', '.'))
    df['setor'] = df['setor'].apply(lambda x: str(x).replace('Ã', 'i'))
    # df['setor'] = df['setor'].apply(lambda x: re.sub(r'Ã ', 'i', x))
    df['codigo'] = df['codigo'].astype('string')
    df['setor'] = df['setor'].astype('string')
    df['precoatualR$'] = pd.to_numeric(df['precoatualR$'], errors='coerce')
    df['liqdiariaNeg'] = pd.to_numeric(df['liqdiariaNeg'], errors='coerce')
    df['dividR$'] = pd.to_numeric(df['dividR$'], errors='coerce')
    df['divyield%'] = pd.to_numeric(df['divyield%'], errors='coerce')
    df['dy3macum%'] = pd.to_numeric(df['dy3macum%'], errors='coerce')
    df['dy6macum%'] = pd.to_numeric(df['dy6macum%'], errors='coerce')
    df['dy12macum%'] = pd.to_numeric(df['dy12macum%'], errors='coerce')
    df['dy3mmedia%'] = pd.to_numeric(df['dy3mmedia%'], errors='coerce')
    df['dy6mmedia%'] = pd.to_numeric(df['dy6mmedia%'], errors='coerce')
    df['dy12mmedia%'] = pd.to_numeric(df['dy12mmedia%'], errors='coerce')
    df['dyano%'] = pd.to_numeric(df['dyano%'], errors='coerce')
    df['varpreco%'] = pd.to_numeric(df['varpreco%'], errors='coerce')
    df['rentper%'] = pd.to_numeric(df['rentper%'], errors='coerce')
    df['rentacum%'] = pd.to_numeric(df['rentacum%'], errors='coerce')
    df['patrliqR$'] = pd.to_numeric(df['patrliqR$'], errors='coerce')
    df['vpaR$'] = pd.to_numeric(df['vpaR$'], errors='coerce')
    df['p/vpaN'] = pd.to_numeric(df['p/vpaN'], errors='coerce')
    df['dypatr%'] = pd.to_numeric(df['dypatr%'], errors='coerce')
    df['varpatr%'] = pd.to_numeric(df['varpatr%'], errors='coerce')
    df['rentpatrper%'] = pd.to_numeric(df['rentpatrper%'], errors='coerce')
    df['rentpatracum%'] = pd.to_numeric(df['rentpatracum%'],
                                        errors='coerce')
    df['vacfisica%'] = pd.to_numeric(df['vacfisica%'], errors='coerce')
    df['vacfinan%'] = pd.to_numeric(df['vacfinan%'], errors='coerce')
    df['qtdativosN'] = pd.to_numeric(df['qtdativosN'], errors='coerce')
    df = df.fillna(0)  # all NaNs filled with zero
    # df['liqdiariaNeg'] = df['liqdiariaNeg'].fillna(0)   # 0 by column
    # df['liqdiariaNeg'] = df['liqdiariaNeg'].replace(np.nan, \
    # 0, regex=True)  # 0 usindg regex
    df['liqdiariaNeg'] = df['liqdiariaNeg'].astype('int64')
    df['qtdativosN'] = df['qtdativosN'].astype('int64')
    return df
