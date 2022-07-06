import json
from typing import Callable, Sequence

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

    df1_renamed = df1.rename(columns=rename_cols) if rename_cols else df1
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


def merge_only_strings(array_of_values: Sequence, separator=' / ') -> str:
    '''Returns a string from an array of values, concatenating only the
        non-empty unique strings (ignores also nan values)

    Args:
        array_of_values (Sequence): the array to filter and join
        separator (str, optional): the separator to use to join the values in
            case the cleaned array has more than 1 value. Defaults to ' / '.

    Returns:
        str: the final string
    '''

    unique_non_null_values = {
        v for v in array_of_values if isinstance(v, str) and v.strip()}

    return separator.join(unique_non_null_values)


def merge_string_columns(
        df: pd.DataFrame,
        column_a: str,
        column_b: str,
) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, removing the duplicated column

    Args:
        df (pd.DataFrame): the original DataFrame
        column_a (str): the name of the column to preserve
        column_b (str): the name of the column to be deleted

    Returns:
        pd.DataFrame: the final DataFrame, with just column_a, but with the
            values from both columns merged
    '''

    local_df = df.copy()

    local_df[column_a] = df[[column_a, column_b]].apply(
        merge_only_strings, axis=1)

    local_df.drop([column_b], axis=1, inplace=True)

    return local_df


def clean_dict_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, cleaning the string column
    formatted as dict, getting only the value of the first key of the dict.
    Works only if the value of the key is a list.

    Args:
        df (pd.DataFrame): the original DataFrame
        column (str): the column name

    Returns:
        pd.DataFrame: the cleaned DataFrame

    eval() function could be used to transform the strings into dictionaries
    an extract the desired key from there, but assuming that the string's
    content may not come from a trusted source, it is better to use the index
    of the string as a way to extract the desired values.

    For that it was assumed that the structure will always be the same:
    a dictionary with only 1 key and the value always a list.

    In any case, it is also provided another method
    (clean_dict_column_insecure), to show the alternative solution.
    '''

    local_df = df.copy()

    local_df[column] = local_df[column].apply(
        lambda s: s[s.find('['):s.find(']')+1])

    return local_df


def clean_dict_column_insecure(
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

    As explained in the method "clean_dict_column", this is not secure because
    it uses the eval() method, that tries to turn any string in Python code,
    which is clearly an insecure operation. Nevertheless, it is a more powerful
    solution, once it provides the possibility to extract the value of a
    specific key and do not rely on the type of the value of the key.
    '''

    local_df = df.copy()

    local_df[column] = local_df[column].apply(
        lambda s: json.dumps(eval(s)[key], ensure_ascii=False))

    return local_df


def clean_stringified_list_insecure(list_as_string: str) -> str:
    '''Creates a copy of the provided stringified list, where the elements are
    the original ones if they are not lists and the elements inside the elements
    if the elements itself are lists. It also remove elements that are empty
    strings.

    Args:
        list_as_string (str): the stringified list to clean

    Returns:
        str: the cleaned copy of the original string
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


def clean_braces_insecure(df: pd.DataFrame, column: str) -> pd.DataFrame:
    '''Creates a copy of the provided DataFrame, cleaning the stringified column
    provided, where the final string representation is a cleaned list, without
    inner lists or empty strings.

    Args:
        df (pd.DataFrame): the original DataFrame
        column (str): the name of the column to be cleaned

    Returns:
        pd.DataFrame: the cleaned DataFrame

    Working simply on the indexes of the string is not optimal here as the
    use of eval() will make it possible to clean other problems than the brace,
    like the object having an empty string or a list with an empty string.

    The use of the eval() is insecure, but was chosen as this is a closed
    environment and the dataset it so small that its content can be verified.
    '''

    local_df = df.copy()

    local_df[column] = local_df[column].apply(
        lambda s: clean_stringified_list_insecure(
            s.strip().replace('{', '[').replace('}', ']')
        )
    )

    return local_df


def make_a_clean_stringified_list_insecure(string: str) -> str:
    '''Clean a list-like string if it is indeed list-like, and if it is a simple
    string return a list-like string with this initial string as its item. The
    returned "list" has only unique values.

    If the provided value is nan, return nan.

    Args:
        string (str): the string to clean

    Returns:
        str: the cleaned list-like string.
    '''

    if pd.isna(string):
        return string

    if not string.startswith('['):
        string = json.dumps([string], ensure_ascii=False)

    return clean_stringified_list_insecure(string)


def remove_duplicated_values_insecure(
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

    As it uses a method that makes use of the eval() method, it is also an
    insecure method.
    '''

    local_df = df.copy()

    for col in list_like_columns:
        local_df[col] = local_df[col].apply(
            make_a_clean_stringified_list_insecure)

    return local_df
