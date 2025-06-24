#!/usr/bin/env python3

def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
import pytest
from server.app import app, db
from flask_migrate import upgrade

@pytest.fixture(scope="module")
def test_client():
    # Use in-memory SQLite database for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Apply migrations to test DB
        upgrade()

        # Create a test client
        testing_client = app.test_client()

        # Provide the test client to tests
        yield testing_client

        # Cleanup after tests
        db.session.remove()
        db.drop_all()
