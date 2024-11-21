"""Database connection and low-level SQL requests."""

import sqlite3
import json
from pathlib import Path
import logging

# Configurez les logs
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def _connect(self):
        """Establish and return a database connection."""
        connection = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES, check_same_thread=False)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def _execute_query(self, query, params=None):
        """Execute a SQL query and return the results."""
        try:
            self.connection = self._connect()
            cursor = self.connection.cursor()
            logging.debug(f"Executing query: {query} | Params: {params}")
            if params:
                result = cursor.execute(query, params).fetchall()
            else:
                result = cursor.execute(query).fetchall()
            logging.debug(f"Query returned {len(result)} rows.")
            self._close()
            return result
        except sqlite3.Error as e:
            logging.error(f"SQL Error: {e}")
            self._close()
            return None


db = Path(__file__).parents[1] / "database" / "olympics.db"
database = Database(db)

TABLES = {
    "country": "country",
    "athlete": "athlete",
    "discipline": "discipline",
    "team": "team",
    "event": "event",
    "medal": "medal",
    "discipline_athlete": "discipline_athlete",
}

def load_queries(file_path):
    """Load SQL queries from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

QUERY_FILE = Path(__file__).parents[0] / "json" / "queries.json"
QUERIES = load_queries(QUERY_FILE)


def get_all_by_id(table, id):
    query = f"SELECT * FROM {table}"
    if id is not None:
        query += " WHERE id = ?"
        return database._execute_query(query, (id,))
    else:
        return database._execute_query(query)


def get_countries(id=None):
    """Get list of countries.

    If id is not None, the list contains only the country with given id.

    """
    return get_all_by_id(TABLES["country"], id)


def get_athletes(id=None):
    """Get list of athletes.

    If id is not None, the list contains only the athlete with given id.

    """
    return get_all_by_id(TABLES["athlete"], id)


def get_disciplines(id=None):
    """Get list of disciplines.

    If id is not None, the list contains only the discipline with given id.

    """
    return get_all_by_id(TABLES["discipline"], id)


def get_teams(id=None):
    """Get list of teams.

    If id is not None, the list contains only the team with given id.

    """
    return get_all_by_id(TABLES["team"], id)


def get_events(id=None):
    """Get list of events.

    If id is not None, the list contains only the event with given id.

    """
    return get_all_by_id(TABLES["event"], id)


def get_medals(id=None):
    """Get list of medals.

    If id is not None, the list contains only the medal with given id.

    """
    return get_all_by_id(TABLES["medal"], id)


def get_discipline_athletes(discipline_id):
    """Get athlete ids linked to given discipline id."""
    return get_all_by_id(TABLES["discipline_athlete"], discipline_id)

def get_top_individual(top=10):
    """Get medal count ranking of athletes for individual events.

    Number of athletes is limited to the given top number.

    """
    query = QUERIES["get_top_individual"]
    return database._execute_query(query, (top,))

def get_top_countries(top=10):
    """Get medal count ranking of countries."""
    query = QUERIES["top_countries"]
    return database._execute_query(query, (top,))


def get_collective_medals(team_id=None):
    """Get list of medals for team events."""
    query = QUERIES["collective_medals"]
    params = (team_id,)
    if team_id:
        query += "  WHERE team.id = ?"
    else: 
        params = None
    return database._execute_query(query, params)


def get_top_collective(top=10):
    """Get medal count ranking of countries for team events."""
    query = QUERIES["top_collective"]
    return database._execute_query(query, (top,))


def get_individual_medals(athlete_id=None):
    """Get list of medals for individual events."""
    query = QUERIES["individual_medals"]
    if athlete_id is not None: 
        query += " WHERE athlete.id = ?"
    return database._execute_query(query, (athlete_id,))
