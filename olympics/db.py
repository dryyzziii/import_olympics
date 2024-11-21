"""Database connection and low-level SQL requests."""

from contextlib import contextmanager
from pathlib import Path
import logging
from sqlalchemy import case, create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func

# Configuration des logs
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration SQLAlchemy
DATABASE_URL = f"sqlite:///{str(Path(__file__).parents[1] / 'database' / 'olympics.db')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modèles
class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    athletes = relationship("Athlete", back_populates="country")
    teams = relationship("Team", back_populates="country")


class Athlete(Base):
    __tablename__ = "athlete"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"))
    gender = Column(String, nullable=False)

    country = relationship("Country", back_populates="athletes")
    medals = relationship("Medal", back_populates="athlete")


class Discipline(Base):
    __tablename__ = "discipline"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    events = relationship("Event", back_populates="discipline")


class Team(Base):
    __tablename__ = "team"
    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("country.id"))

    country = relationship("Country", back_populates="teams")
    medals = relationship("Medal", back_populates="team")


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    discipline_id = Column(Integer, ForeignKey("discipline.id"))

    discipline = relationship("Discipline", back_populates="events")
    medals = relationship("Medal", back_populates="event")

class DisciplineAthlete(Base):
    __tablename__ = "discipline_athlete"
    id = Column(Integer, primary_key=True, index=True)
    discipline_id = Column(Integer, ForeignKey("discipline.id"), primary_key=True)
    athlete_id = Column(Integer, ForeignKey("athlete.id"), primary_key=True)



class Medal(Base):
    __tablename__ = "medal"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  # 'gold', 'silver', 'bronze'
    athlete_id = Column(Integer, ForeignKey("athlete.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("team.id"), nullable=True)
    event_id = Column(Integer, ForeignKey("event.id"))
    date = Column(Date, nullable=True)

    athlete = relationship("Athlete", back_populates="medals")
    team = relationship("Team", back_populates="medals")
    event = relationship("Event", back_populates="medals")


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Session rollback because of {e}")
        raise
    finally:
        session.close()

def get_all_by_id(session, model, id=None):
    """Fetch all rows or by ID from a model."""
    if id:
        return session.query(model).filter(model.id == id).all()
    return session.query(model).all()


def get_countries(id=None):
    with get_session() as session:
        return get_all_by_id(session, Country, id)


def get_athletes(id=None):
    with get_session() as session:
        return get_all_by_id(session, Athlete, id)


def get_disciplines(id=None):
    with get_session() as session:
        return get_all_by_id(session, Discipline, id)


def get_teams(id=None):
    with get_session() as session:
        return get_all_by_id(session, Team, id)


def get_events(id=None):
    with get_session() as session:
        return get_all_by_id(session, Event, id)


def get_medals(id=None):
    with get_session() as session:
        return get_all_by_id(session, Medal, id)


def get_discipline_athletes(discipline_id=None):
    with get_session() as session:
        return get_all_by_id(session, DisciplineAthlete, discipline_id)



def get_top_individual(top=10):
    """Get the top individual athletes by medal count."""
    with get_session() as session:
        result = (
            session.query(
                Athlete.name.label("name"),
                Athlete.gender.label("gender"),
                Country.name.label("country"),
                func.count(Medal.id).label("medals"),
            )
            .join(Medal, Medal.athlete_id == Athlete.id)
            .join(Country, Athlete.country_id == Country.id)
            .group_by(Athlete.name, Athlete.gender, Country.name)
            .order_by(func.count(Medal.id).desc())
            .limit(top)
            .all()
        )
        # Convertir les résultats en dictionnaires
        return [row._asdict() if hasattr(row, '_asdict') else dict(row._mapping) for row in result]



def get_top_countries(top=10):
    with get_session() as session:
        result = (
            session.query(
                Country.name.label("country"),
                func.sum(case((Medal.type == "gold", 1), else_=0)).label("gold"),
                func.sum(case((Medal.type == "silver", 1), else_=0)).label("silver"),
                func.sum(case((Medal.type == "bronze", 1), else_=0)).label("bronze"),
            )
            .outerjoin(Team, Team.country_id == Country.id)
            .outerjoin(Medal, Medal.team_id == Team.id)
            .group_by(Country.id)
            .order_by(
                func.sum(case((Medal.type == "gold", 1), else_=0)).desc(),
                func.sum(case((Medal.type == "silver", 1), else_=0)).desc(),
                func.sum(case((Medal.type == "bronze", 1), else_=0)).desc(),
            )
            .limit(top)
            .all()
        )
        return [dict(row._mapping) for row in result]


def get_collective_medals(team_id=None):
    """Get a list of medals for a specific team or all team events."""
    with get_session() as session:
        query = (
            session.query(
                Country.name.label("country"),
                Discipline.name.label("discipline"),
                Event.name.label("event"),
                Medal.type.label("medal_type"),
                Medal.date.label("date"),
            )
            .join(Team, Medal.team_id == Team.id)
            .join(Country, Team.country_id == Country.id)
            .join(Event, Medal.event_id == Event.id)
            .join(Discipline, Event.discipline_id == Discipline.id)
        )

        if team_id:
            query = query.filter(Team.id == team_id)

        result = query.all()
        # Conversion en dictionnaires
        return [dict(row._mapping) for row in result]



def get_top_collective(top=10):
    """Get the top countries by collective medal count."""
    with get_session() as session:
        result = (
            session.query(
                Country.name.label("country"),
                func.count(Medal.id).label("medals"),
            )
            .join(Team, Medal.team_id == Team.id)
            .join(Country, Team.country_id == Country.id)
            .group_by(Country.id)
            .order_by(func.count(Medal.id).desc())
            .limit(top)
            .all()
        )
        # Conversion en dictionnaires
        return [dict(row._mapping) for row in result]



def get_individual_medals(athlete_id=None):
    """Get a list of medals for individual athletes."""
    with get_session() as session:
        query = (
            session.query(
                Athlete.name.label("name"),
                Country.name.label("country"),
                Discipline.name.label("discipline"),
                Event.name.label("event"),
                Medal.type.label("medal_type"),
                Medal.date.label("date"),
            )
            .join(Medal, Medal.athlete_id == Athlete.id)
            .join(Country, Athlete.country_id == Country.id)
            .join(Event, Medal.event_id == Event.id)
            .join(Discipline, Event.discipline_id == Discipline.id)
        )
        if athlete_id:
            query = query.filter(Athlete.id == athlete_id)

        result = query.all()
        # Conversion en dictionnaires
        return [dict(row._mapping) for row in result]

