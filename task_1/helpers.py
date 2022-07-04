from copy import deepcopy
from typing import Callable

import pandas as pd
import pycountry


def concat_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    rename_cols: dict[str, str] = None,
) -> pd.DataFrame:
    '''Creates a concatenated DataFrame from the provide DataFrames. It also
        renames the columns of the first df according to the provided dictionary

    Args:
        df1 (pd.DataFrame): the DataFrame which columns will be renamed
        df2 (pd.DataFrame): the DataFrame which column names will be preserved
        rename_cols (dict[str, str], optional): a dictionary structured as
            {'column_to_be_renamed': 'new_column_name'}. Defaults to None.

    Returns:
        pd.DataFrame: the concatenated DataFrame, with the column names of the
            second DataFrame
    '''

    # The TODOS need to be handled when creating the package
    # TODO: verify that the number of columns of both dfs match

    df1_renamed = df1.rename(columns=rename_cols) if rename_cols else df1

    # TODO: verify that the name of the columns of both dfs match
    # TODO: an exception type may need to be created to raise that

    df_concatenated = pd.concat([df1_renamed, df2])

    return df_concatenated


def clean_columns_values(
    df: pd.DataFrame,
    columns: list[str],
    operation: Callable = str.capitalize,
    replaces: dict[str, dict[str, str]] = None,
) -> pd.DataFrame:
    '''Creates a copy of the original DataFrame, performing the operation on the
        specified columns, besides replacing a set of specified words in each
        column

    Args:
        df (pd.DataFrame): the base DataFrame
        columns (list[str]): the list of columns to be fixed
        operation (Callable, optional): the operation to be performed in each
            column. Defaults to str.capitalize.
        replaces (dict[str, dict[str, str]], optional): the columns which to
            replace values (if any) and the values.

    Returns:
        pd.DataFrame: the cleaned DataFrame, with the column names of the second
            DataFrame

    >>> replace_words = {'colA': {'Old': 'New'}}
    >>> clean_columns_values(df, ['colA', 'colB], str.lower, replace_words)
    '''

    local_df = df.copy()
    for col in columns:
        local_df[col] = local_df[col].apply(operation)

        if replaces and col in replaces:
            words_to_replace = replaces[col]

            # "w" stands for "word"
            local_df[col] = local_df[col].apply(
                lambda w: words_to_replace[w] if w in words_to_replace else w)

    return local_df


def format_country(country: str, format: str = 'alpha_2') -> str:
    '''Gives the proper name of a country according to a specific format

    Args:
        country (str): the string to search for. It can be any official value,
            e.g. GB / GBR / United Kingdom
        format (str): the desired output format for the country name (it needs
            to be a valid attribute of the pycountry object). Defaults to
            'alpha_2'.

    Returns:
        str: the country name properly formatted.
    '''

    # Strip the name so it don't brake during the interaction with pycountry
    country = country.strip()

    # Special cases that need treatment
    special_cases = {
        'UK': 'GB'
    }

    if country.upper() in special_cases:
        country = 'GB'

    return getattr(pycountry.countries.lookup(country), format)


def fix_country_columns(
        df: pd.DataFrame,
        columns: list[str],
        format: str = 'alpha_2',
) -> pd.DataFrame:
    '''Creates a copy of the original DataFrame, standardizing the country names
        on the provided columns with the format desired

    Args:
        df (pd.DataFrame): the base DataFrame
        columns (list[str]): the list of columns to be fixed
        format (str, optional): format (str): the desired output format for the
            country name (it needs to be a valid attribute of the pycountry
            object). Defaults to 'alpha_2'.

    Returns:
        pd.DataFrame: the cleaned DataFrame
    '''

    local_df = df.copy()

    for col in columns:
        local_df[col] = local_df[col].apply(
            lambda country: format_country(country, format))

    return local_df
