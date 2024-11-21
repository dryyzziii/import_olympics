from olympics import db

def test_countries_with_id():
    rows = db.get_countries(1)
    assert rows is not None, "get_countries(1) returned None"
    assert len(rows) == 1

def test_athletes():
    rows = db.get_athletes()
    assert rows is not None, "get_athletes() returned None"
    assert len(rows) > 100

def test_athletes_with_id():
    rows = db.get_athletes(1)
    assert rows is not None, "get_athletes(1) returned None"
    assert len(rows) == 1

def test_disciplines():
    rows = db.get_disciplines()
    assert rows is not None, "get_disciplines() returned None"
    assert len(rows) > 40

def test_disciplines_with_id():
    rows = db.get_disciplines(1)
    assert rows is not None, "get_disciplines(1) returned None"
    assert len(rows) == 1

def test_teams():
    rows = db.get_teams()
    assert rows is not None, "get_teams() returned None"
    assert len(rows) > 100

def test_teams_with_id():
    rows = db.get_teams(1)
    assert rows is not None, "get_teams(1) returned None"
    assert len(rows) == 1

def test_events():
    rows = db.get_events()
    assert rows is not None, "get_events() returned None"
    assert len(rows) > 100

def test_events_with_id():
    rows = db.get_events(1)
    assert rows is not None, "get_events(1) returned None"
    assert len(rows) == 1

def test_medals():
    rows = db.get_medals()
    assert rows is not None, "get_medals(1) returned None"
    assert len(rows) > 100

def test_medals_with_id():
    rows = db.get_medals(1)
    assert rows is not None, "get_medals(1) returned None"
    assert len(rows) == 1

def test_individual_medals():
    rows = db.get_individual_medals(1)
    assert rows is not None, "get_individual_medals(1) returned None"
    assert len(rows) < 100

def test_get_collective_medals():
    rows = db.get_collective_medals()
    assert rows is not None, "get_medals() returned None"
    assert len(rows) > 100

def test_get_collective_medals_by_id():
    rows = db.get_collective_medals(3)
    assert rows is not None, "get_individual_medals(1) returned None"
    assert len(rows) == 1
