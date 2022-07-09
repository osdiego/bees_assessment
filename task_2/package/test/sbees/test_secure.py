import pytest
from src.sbees.secure import format_country


@pytest.mark.parametrize(
    ('input, expected, format'),
    [
        ('United Kingdom', 'GB', 'alpha_2'),
        ('GB', 'GB', 'alpha_2'),
        ('UK', 'GB', 'alpha_2'),
        ('UniTed KINGdoM', 'GB', 'alpha_2'),
        ('UK', 'GBR', 'alpha_3'),
    ],
    ids=[
        'UK_full_name',
        'UK_code',
        'UK_not_standard_code',
        'UK_mixed_case',
        'UK_alpha_3',
    ]
)
@pytest.mark.unittest
def test_format_country(input: str, expected: str, format: str) -> None:
    assert expected == format_country(country=input, format=format)
