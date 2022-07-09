import pandas as pd
import pytest
from src.sbees.insecure import (clean_stringified_list,
                                make_a_clean_stringified_list,
                                remove_duplicated_values)


@pytest.mark.parametrize(
    ('input, expected'),
    [
        ('["birds", "bees", "bees"]', '["bees", "birds"]'),
        ('["birds", "", "bees"]', '["bees", "birds"]'),
        ('["birds", "bees", "", "bees"]', '["bees", "birds"]'),
    ],
    ids=[
        'remove_duplicated_items',
        'remove_empty_strings',
        'remove_duplicated_and_empty',
    ]
)
@pytest.mark.unittest
def test_clean_stringified_list(input: str, expected: str) -> None:
    assert expected == clean_stringified_list(list_as_string=input)


@pytest.mark.parametrize(
    ('input, expected'),
    [
        ('["birds", "bees", "bees"]', '["bees", "birds"]'),
        ('["birds", "", "bees"]', '["bees", "birds"]'),
        ('["birds", "bees", "", "bees"]', '["bees", "birds"]'),
        ('bees', '["bees"]'),
        (pd.NA, pd.NA),
    ],
    ids=[
        'remove_duplicated_items_from_list_like_string',
        'remove_empty_strings_from_list_like_string',
        'remove_duplicated_and_empty_from_list_like_string',
        'turn_string_into_list_like_string',
        'nan_return_nan',
    ]
)
@pytest.mark.unittest
def test_make_a_clean_stringified_list(input: str, expected: str) -> None:
    if isinstance(input, str):
        assert expected == make_a_clean_stringified_list(string=input)
    else:
        assert pd.isna(expected) and pd.isna(input)


@pytest.mark.unittest
def test_remove_duplicated_values(df: pd.DataFrame) -> None:
    df_expected = df.drop(['input'], axis=1).rename(
        columns={'expected': 'input'})

    df_input = remove_duplicated_values(
        df=df.drop(['expected'], axis=1),
        list_like_columns=['input']
    )

    pd.testing.assert_frame_equal(df_expected, df_input)
