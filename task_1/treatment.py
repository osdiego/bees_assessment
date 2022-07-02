import logging
from typing import Callable

import pandas as pd


def concat_dataframes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    rename_cols: dict[str, str] = None,
) -> pd.DataFrame:
    '''Concatenate the provide dataframes. It also renames the columns of the
    first df according to the provided dictionary.

    Args:
        df1 (pd.DataFrame): the df which columns will be renamed
        df2 (pd.DataFrame): the df which column names will be preserved
        rename_cols (dict[str, str], optional): a dictionary structured as
            {'column_to_be_renamed': 'new_column_name'}. Defaults to None.

    Returns:
        pd.DataFrame: the concatenated df, with the column names of the second df
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
    replaces: dict[str, dict[str, str]] = dict(),
) -> pd.DataFrame:

    local_df = df.copy()
    for col in columns:
        local_df[col] = local_df[col].apply(operation)

        if col in replaces:
            words_to_replace = replaces[col]

            # w stands for "word"
            local_df[col] = local_df[col].apply(
                lambda w: words_to_replace[w] if w in words_to_replace else w)

    return local_df


def main():
    # To run the script inside the task_1 folder
    assets_folder = '../assets/'
    # to run it directly on the root folder
    # assets_folder = './assets/'

    # Read csv files into pandas DataFrames to better understanding
    df_bg_map = pd.read_csv(f'{assets_folder}background_mapping.csv')
    clean_columns = {c: c.strip() for c in df_bg_map}
    df_bg_map.rename(columns=clean_columns, inplace=True)

    df_bg_1 = pd.read_csv(f'{assets_folder}project_1_background.csv')
    df_bg_2 = pd.read_csv(f'{assets_folder}project_2_background.csv')

    df_logs_1 = pd.read_csv(f'{assets_folder}project_1_logs.csv')
    df_logs_2 = pd.read_csv(f'{assets_folder}project_2_logs.csv')

    # Verify the difference between the background df schemas
    is_bg_schemas_equal = sorted(list(df_bg_1)) == sorted(list(df_bg_2))
    logger.debug(
        f'Background schemas are equal? Answer: {is_bg_schemas_equal}')

    bg1_not_in_bg2 = sorted([c for c in df_bg_1 if c not in df_bg_2])
    bg2_not_in_bg1 = sorted([c for c in df_bg_2 if c not in df_bg_1])

    # Verify that the difference between dfs are the ones in the mapping
    prj_2_cols = sorted(df_bg_map['Project 1 Question'].values.tolist())
    is_prj_2_cols_mapped = prj_2_cols == bg2_not_in_bg1
    prj_1_cols = sorted(df_bg_map['Project 2 Question'].values.tolist())
    is_prj_1_cols_mapped = prj_1_cols == bg1_not_in_bg2

    # and that the columns in the mapping file are indeed switched
    is_all_columns_mapped = is_prj_2_cols_mapped and is_prj_1_cols_mapped
    logger.debug(
        'The columns in the mapping represents all the mismatched columns' +
        f' in background DataFrames: {is_all_columns_mapped}'
    )

    # Confirm that the log dfs has the same schema
    is_logs_schemas_equal = sorted(list(df_logs_1)) == sorted(list(df_logs_2))
    logger.debug(f'Logs schemas are equal? Answer: {is_logs_schemas_equal}')

    # Merge dfs - the project 2 columns will be used as final column names
    map_bg_cols = dict(zip(prj_1_cols, prj_2_cols))
    df_logs = concat_dataframes(df1=df_logs_1, df2=df_logs_2)
    df_bg = concat_dataframes(
        df1=df_bg_1, df2=df_bg_2, rename_cols=map_bg_cols)

    # Fix genders spelt / capitalized differently
    col_gender = 'questions_135556_what_is_your_gender'
    df_bg = clean_columns_values(df=df_bg, columns=[col_gender])

    # It shows that "Demale" exists, what is clearly a mistake
    logger.debug(set(df_bg[col_gender].values))

    # And now it is fixed (done in 2 steps to show the error)
    map_to_replace = {col_gender: {'Demale': 'Female'}}
    df_bg = clean_columns_values(
        df=df_bg, columns=[col_gender], replaces=map_to_replace)
    logger.debug(set(df_bg[col_gender].values))

    logger.info('The end.')


# As best practice
if __name__ == '__main__':
    format_str = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=format_str)

    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    f_handler = logging.FileHandler('task_1.log')
    f_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    format = logging.Formatter(format_str)
    f_handler.setFormatter(format)

    # Add handlers to the logger
    logger.addHandler(f_handler)

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    pd.set_option('max_colwidth', 400)

    main()
