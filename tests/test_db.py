from olympics import db
import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect
from olympics.db import get_session, Country, engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

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
    for row in rows:
        assert "name" in row
        assert "country" in row
        assert "discipline" in row
        assert "event" in row
        assert "medal_type" in row
        assert "date" in row



def test_collective_medals():
    rows = db.get_collective_medals()
    assert rows is not None, "get_collective_medals() returned None"
    assert len(rows) > 0
    for row in rows:
        assert "country" in row
        assert "discipline" in row
        assert "event" in row
        assert "medal_type" in row
        assert "date" in row

def test_get_collective_medals_by_id():
    # Test avec team_id
    rows = db.get_collective_medals(3)
    assert rows is not None, f"get_collective_medals({3}) returned None"
    assert len(rows) > 0



def test_top_collective():
    rows = db.get_top_collective(10)
    assert rows is not None, "get_top_collective() returned None"
    assert len(rows) > 0
    for row in rows:
        assert "country" in row
        assert "medals" in row

@pytest.fixture
def setup_database():
    # Nettoyer la base de données avant chaque test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Nettoyer la base de données après chaque test
    Base.metadata.drop_all(bind=engine)


def test_session_rollback(setup_database):
    with pytest.raises(IntegrityError):  # On s'attend à une erreur d'intégrité
        with get_session() as session:
            # Ajouter deux pays avec le même nom pour provoquer une violation de contrainte unique
            country1 = Country(name="Duplicate Country")
            country2 = Country(name="Duplicate Country")
            session.add(country1)
            session.add(country2)  # Cela devrait déclencher une exception
    # Vérifier que rien n'a été ajouté à la base de données
    with get_session() as session:
        result = session.query(Country).filter_by(name="Duplicate Country").all()
        assert len(result) == 0

def test_session_exception_handling(setup_database):
    with pytest.raises(ValueError, match="Test Exception"):
        with get_session() as session:
            # Ajouter un pays
            country = Country(name="Rollback Test")
            session.add(country)
            # Lever une exception volontairement
            raise ValueError("Test Exception")
    # Vérifier que le rollback a fonctionné
    with get_session() as session:
        result = session.query(Country).filter_by(name="Rollback Test").one_or_none()
        assert result is None
