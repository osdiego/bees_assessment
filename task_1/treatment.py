'''
The unused imports (pprint and clean_dict_column_insecure) were kept because
there is some commented code that uses it, and it may be uncommented during
the assessment.
'''

import json
import logging
from pprint import pprint

import pandas as pd

from helpers import (clean_braces_insecure, clean_columns_values,
                     clean_dict_column, clean_dict_column_insecure,
                     concat_dataframes, fix_country_columns,
                     merge_string_columns, remove_duplicated_values_insecure)


def main():
    # ||| Step 1 |||: read csv files into pandas DataFrames to better understanding
    # To run the script inside the task_1 folder
    assets_folder = '../assets/'
    # to run it directly on the root folder
    # assets_folder = './assets/'

    df_bg_map = pd.read_csv(f'{assets_folder}background_mapping.csv')
    clean_columns = {c: c.strip() for c in df_bg_map}
    df_bg_map.rename(columns=clean_columns, inplace=True)

    df_bg_1 = pd.read_csv(
        f'{assets_folder}project_1_background.csv', index_col=0)
    df_bg_2 = pd.read_csv(
        f'{assets_folder}project_2_background.csv', index_col=0)

    df_logs_1 = pd.read_csv(
        f'{assets_folder}project_1_logs.csv', index_col=0)
    df_logs_2 = pd.read_csv(
        f'{assets_folder}project_2_logs.csv', index_col=0)

    # ||| Step 2 |||: check the difference between datasets
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

    # ||| Step 3 |||: solve problem on column "level2dish_coded"
    '''For performance reasons, it is necessary to do some cleaning on the
    datasets before doing the merge'''
    # Check the real problem in the column formatted as dictionary
    # pprint(sorted(set(df_logs_1['level2dish_coded'].values)))

    # Extract the desired value from the column
    df_logs_1 = clean_dict_column(df=df_logs_1, column='level2dish_coded')
    # What could be also achieved using the insecure method:
    # df_logs_1 = clean_dict_column_insecure(df=df_logs_1, column='level2dish_coded', key='dish')

    # ||| Step 4 |||: solve problem on column "questions_135633_and_who_are_you_sharing_your_home_with"
    # check the real problem in the column
    column_135633 = 'questions_135633_and_who_are_you_sharing_your_home_with'
    # pprint(sorted(set(df_bg_1[column_135633].values)))
    # not all values has the brace problem, so the function created handles that
    df_bg_1 = clean_braces_insecure(df=df_bg_1, column=column_135633)
    # pprint(sorted(set(df_bg_1[column_135633].values)))

    # ||| Step 5 |||: merge DataFrames
    # the project 2 columns will be used as final column names
    map_bg_cols = dict(zip(prj_1_cols, prj_2_cols))
    df_logs = concat_dataframes(df1=df_logs_1, df2=df_logs_2)
    df_bg = concat_dataframes(
        df1=df_bg_1, df2=df_bg_2, rename_cols=map_bg_cols)

    # ||| Step 6 |||: fix genders spelt / capitalized differently
    col_gender = 'questions_135556_what_is_your_gender'
    df_bg = clean_columns_values(df=df_bg, columns=[col_gender])

    # It shows that "Demale" exists, what is clearly a mistake
    logger.debug(set(df_bg[col_gender].values))

    # And now it is fixed (done in 2 steps to show the error)
    map_to_replace = {col_gender: {'Demale': 'Female'}}
    df_bg = clean_columns_values(
        df=df_bg, columns=[col_gender], replaces=map_to_replace)
    logger.debug(set(df_bg[col_gender].values))

    # ||| Step 7 |||: set all location names to codes
    # 1º: verify the severity of the problem
    logger.debug(sorted(set(df_logs['location_name'].values)))

    # 2ª: fix the problem - small note on conversion UK -> GB as this is the ISO
    df_logs = fix_country_columns(df=df_logs, columns=['location_name'])
    logger.debug(sorted(set(df_logs['location_name'].values)))

    # ||| Step 8 |||: merge duplicated columns
    # Verify the existence of duplicated columns on the DataFrames
    # pprint(sorted(set(df_bg.columns)))
    # pprint(sorted(set(df_logs.columns)))

    '''This shows that the questions_134999_where_are_you_eating_at_the_moment
    column is duplicated on df_logs and will need to be merged, and now it can
    be done'''
    df_logs = merge_string_columns(
        df=df_logs,
        column_a='questions_134999_where_are_you_eating_at_the_moment',
        column_b='questions_134999_where_are_you_eating_at_the_moment.1')

    # ||| Step 9 |||: merge duplicated values on specific columns
    '''
    First is necessary to understand which columns will need to be cleaned,
    and for that specific case, as it is going to be a massive cleaning,
    discover dynamically which columns need it would not be a safe / optimal
    choice, so the columns that needs the treatment were verified "simply" by
    looking at the data and checking the ones that have an structure of a list.
    The columns were then mapped and placed into an asset file.
    '''
    with open('./list_like_columns_map.json') as file:
        list_like_columns_map = json.load(file)
    # pprint(list_like_columns_map)

    df_bg = remove_duplicated_values_insecure(
        df=df_bg, list_like_columns=list_like_columns_map['background'])

    df_logs = remove_duplicated_values_insecure(
        df=df_logs, list_like_columns=list_like_columns_map['logs'])

    # ||| Step 10 |||: save the DataFrames
    '''Both DataFrames are too large to print nicely, so they're being saved as
    XLSX for a better visualization - could be also saved as CSV, Parquet, etc.
    '''
    df_bg.to_excel('output/background_dataset.xlsx')
    df_logs.to_excel('output/logs_dataset.xlsx')

    logger.info('The end.')


# As best practice and to avoid running code unintentionally
if __name__ == '__main__':
    # Configure the logs is the first thing on the file
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

    # Configure the settings of pandas so the DataFrames can be better printed
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)
    pd.set_option('max_colwidth', 400)

    main()
