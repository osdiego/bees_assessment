'''All the global available fixtures are written here.'''

import pandas as pd
import pytest


@pytest.fixture(scope='session')
def assets_folder() -> str:
    return './test/sbees/assets/'


@pytest.fixture(scope='session')
def df_base(assets_folder: str) -> pd.DataFrame:
    return pd.read_csv(f'{assets_folder}test_data.csv', index_col=0)


@pytest.fixture(scope='function')
def df(df_base: pd.DataFrame) -> pd.DataFrame:
    '''Create a DataFrame to be used for the tests in all functions.

    To avoid changing the DataFrame in place and it end affecting other
    tests, the scope of this fixture is set "function".
    '''
    return df_base.copy()
