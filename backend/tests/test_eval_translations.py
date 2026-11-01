import pytest

from evals.eval_translations import match_trailing_period


# parametrize esegue lo stesso test una volta per ogni tupla (come un
# @dataProvider di PHPUnit).
@pytest.mark.parametrize(
    ("source", "translation", "expected"),
    [
        ("Fare il letto", "Het bed opmaken.", "Het bed opmaken"),
        ("Leggere 15 minuti", "Lezen: 15 minuten.", "Lezen: 15 minuten"),
        ("Fare il letto.", "Het bed opmaken.", "Het bed opmaken."),
        ("Fare il letto", "Het bed opmaken", "Het bed opmaken"),
        ("Serata cinema", "Filmavond...", "Filmavond"),
        ("Aspetta...", "Wacht...", "Wacht..."),
    ],
)
def test_match_trailing_period(source: str, translation: str, expected: str) -> None:
    assert match_trailing_period(source, translation) == expected
