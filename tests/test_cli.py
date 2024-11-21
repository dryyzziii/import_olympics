from io import StringIO

from olympics import cli


def test_top_countries():
    string = StringIO()
    cli.top_countries(file=string)
    text = string.getvalue()
    assert 'Top' in text

def test_top_collective():
    string = StringIO()
    cli.top_collective(file=string)
    text = string.getvalue()
    assert 'Top' in text

def test_top_individual():
    string = StringIO()
    cli.top_individual(file=string)
    text = string.getvalue()
    assert 'Top' in text
