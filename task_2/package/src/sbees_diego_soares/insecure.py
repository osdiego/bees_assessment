import json

import pandas as pd


def clean_dict_column(
    df: pd.DataFrame,
    column: str,
    key: str,
) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, cleaning the string column
    formatted as dict, getting the value of the provided key.

    Args:
        df (pd.DataFrame): the original DataFrame
        column (str): the column name
        key (str): the key from where to get the return value

    Returns:
        pd.DataFrame: the cleaned DataFrame

    DISCLAIMER: This is considered a not secure method because it uses the
    eval() method, that tries to turn any string into Python code, which is
    clearly an insecure operation. It is not recommended to use this method in a
    non-trusted dataset.
    '''

    local_df = df.copy()

    local_df[column] = local_df[column].apply(
        lambda s: json.dumps(eval(s)[key], ensure_ascii=False))

    return local_df


def clean_stringified_list(list_as_string: str) -> str:
    '''Creates a copy of the provided stringified list, where the elements are
    the original ones if they are not lists and the elements inside the elements
    if the elements itself are lists. It also remove elements that are empty
    strings.

    Args:
        list_as_string (str): the stringified list to clean

    Returns:
        str: the cleaned copy of the original string

    DISCLAIMER: This is considered a not secure method because it uses the
    eval() method, that tries to turn any string into Python code, which is
    clearly an insecure operation. It is not recommended to use this method in a
    non-trusted dataset.
    '''

    list_as_list = eval(list_as_string)
    temp_set = set()

    for value in list_as_list:
        if isinstance(value, list):
            for inner_value in value:
                temp_set.add(inner_value)
        else:
            temp_set.add(value)

    return json.dumps([v for v in temp_set if v], ensure_ascii=False)


def clean_braces(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, cleaning the stringified column
    provided, where the final string representation is a cleaned list, without
    inner lists or empty strings.

    Args:
        df (pd.DataFrame): the original DataFrame
        column (str): the name of the column to be cleaned

    Returns:
        pd.DataFrame: the cleaned DataFrame

    DISCLAIMER: This is considered a not secure method because it uses the
    eval() method, that tries to turn any string into Python code, which is
    clearly an insecure operation. It is not recommended to use this method in a
    non-trusted dataset.
    '''

    local_df = df.copy()

    local_df[column] = local_df[column].apply(
        lambda s: clean_stringified_list(
            s.strip().replace('{', '[').replace('}', ']')
        )
    )

    return local_df


def make_a_clean_stringified_list(string: str) -> str:
    '''Clean a list-like string if it is indeed list-like, and if it is a simple
    string return a list-like string with this initial string as its item. The
    returned "list" has only unique values.

    If the provided value is nan, return nan.

    Args:
        string (str): the string to clean

    Returns:
        str: the cleaned list-like string.

    DISCLAIMER: This is considered a not secure method because it uses the
    eval() method, that tries to turn any string into Python code, which is
    clearly an insecure operation. It is not recommended to use this method in a
    non-trusted dataset.
    '''

    if pd.isna(string):
        return string

    if not string.startswith('['):
        string = json.dumps([string], ensure_ascii=False)

    return clean_stringified_list(string)


def remove_duplicated_values(
    df: pd.DataFrame,
    list_like_columns: list[str],
) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, turning the values in each list
    like columns unique

    Args:
        df (pd.DataFrame): the original DataFrame
        list_like_columns (list[str]): the columns names to apply to cleaning

    Returns:
        pd.DataFrame: the DataFrame with the unique values

    DISCLAIMER: This is considered a not secure method because it uses the
    eval() method, that tries to turn any string into Python code, which is
    clearly an insecure operation. It is not recommended to use this method in a
    non-trusted dataset.
    '''

    local_df = df.copy()

    for col in list_like_columns:
        local_df[col] = local_df[col].apply(
            make_a_clean_stringified_list)

    return local_df
