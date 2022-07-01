import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('max_colwidth', 400)

if __name__ == '__main__':
    assets_folder = './assets/'

    # Read csv files into pandas DataFrames to better understanding
    df_bg_map = pd.read_csv(f'{assets_folder}background_mapping.csv')
    clean_columns = {c: c.strip()for c in df_bg_map}
    df_bg_map.rename(columns=clean_columns, inplace=True)

    df_bg_1 = pd.read_csv(f'{assets_folder}project_1_background.csv')
    df_bg_2 = pd.read_csv(f'{assets_folder}project_2_background.csv')

    df_logs_1 = pd.read_csv(f'{assets_folder}project_1_logs.csv')
    df_logs_2 = pd.read_csv(f'{assets_folder}project_2_logs.csv')

    # Verify the difference between the background df schemas
    is_bg_schemas_equal = sorted(list(df_bg_1)) == sorted(list(df_bg_2))
    print(f'\nBackground schemas are equal? Answer: {is_bg_schemas_equal}')

    bg1_not_in_bg2 = sorted([c for c in df_bg_1 if c not in df_bg_2])
    bg2_not_in_bg1 = sorted([c for c in df_bg_2 if c not in df_bg_1])

    # Verify that the difference between dfs are the ones in the mapping
    prj_1_cols = sorted(df_bg_map['Project 1 Question'].values.tolist())
    prj_2_cols = sorted(df_bg_map['Project 2 Question'].values.tolist())

    # Verify that the columns in the mapping file are actually switched
    is_all_columns_mapped = prj_1_cols == bg2_not_in_bg1 \
        and prj_2_cols == bg1_not_in_bg2
    print(
        'The columns in the mapping represents all the mismatched columns' +
        f' in background DataFrames: {is_all_columns_mapped}'
    )

    # Confirm that the log dfs has the same schema
    is_logs_schemas_equal = sorted(list(df_logs_1.columns))\
        == sorted(list(df_logs_2.columns))
    print(f'Logs schemas are equal? Answer: {is_logs_schemas_equal}')
