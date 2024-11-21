from olympics import db

def test_countries():
    rows = db.get_countries()
    assert len(rows) > 100

def test_countries_with_id():
    rows = db.get_countries(1)
    assert len(rows) == 1

def test_athletes():
    rows = db.get_athletes()
    assert len(rows) > 100

def test_athletes_with_id():
    rows = db.get_athletes(1)
    assert len(rows) == 1

def test_disciplines():
    rows = db.get_disciplines()
    assert len(rows) > 40

def test_disciplines_with_id():
    rows = db.get_disciplines(1)
    assert len(rows) == 1

def test_teams():
    rows = db.get_teams()
    assert len(rows) > 100

def test_teams_with_id():
    rows = db.get_teams(1)
    assert len(rows) == 1

def test_events():
    rows = db.get_events()
    assert len(rows) > 100

def test_events_with_id():
    rows = db.get_events(1)
    assert len(rows) == 1

def test_medals():
    rows = db.get_medals()
    assert len(rows) > 100

def test_medals_with_id():
    rows = db.get_medals(1)
    assert len(rows) == 1

def test_individual_medals():
    rows = db.get_individual_medals(1)
    assert len(rows) < 100 