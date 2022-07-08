import pytest
from src.sbees.insecure import clean_stringified_list


@pytest.fixture
def list_like_string() -> str:
    return '["Male", "Female"]'


@pytest.mark.unittest
def test_clean_stringified_list() -> None:
    string = '["bees", "bees", ""]'
    result = clean_stringified_list(string)
    expected = '["bees"]'

    assert expected == result
