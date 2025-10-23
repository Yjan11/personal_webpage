"""
Pytest configuration and shared fixtures for the Flask website tests.
"""

import pytest
import tempfile
import os
import sqlite3
from flask import Flask
from app import app


@pytest.fixture(scope="session")
def test_database():
    """Create a temporary test database for the entire test session."""
    # Create a temporary database file
    test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    test_db.close()
    
    # Create the database structure
    conn = sqlite3.connect(test_db.name)
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Description TEXT NOT NULL,
            ImageFileName TEXT NOT NULL,
            Technologies TEXT,
            GitHubLink TEXT,
            DemoLink TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    yield test_db.name
    
    # Cleanup
    if os.path.exists(test_db.name):
        os.unlink(test_db.name)


@pytest.fixture
def flask_app():
    """Create a Flask app instance for testing."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


@pytest.fixture
def client(flask_app):
    """Create a test client for the Flask app."""
    return flask_app.test_client()


@pytest.fixture
def sample_project_data():
    """Provide sample project data for testing."""
    return {
        'title': 'Sample Project',
        'description': 'This is a sample project for testing',
        'image_filename': 'sample.png',
        'technologies': 'Python, Flask, SQLite',
        'github_link': 'https://github.com/sample/project',
        'demo_link': 'https://demo.sample.com'
    }


@pytest.fixture
def multiple_projects_data():
    """Provide multiple sample projects for testing."""
    return [
        {
            'title': 'Project 1',
            'description': 'First test project',
            'image_filename': 'project1.png',
            'technologies': 'Python',
            'github_link': 'https://github.com/test1',
            'demo_link': 'https://demo1.test'
        },
        {
            'title': 'Project 2',
            'description': 'Second test project',
            'image_filename': 'project2.png',
            'technologies': 'JavaScript',
            'github_link': 'https://github.com/test2',
            'demo_link': 'https://demo2.test'
        },
        {
            'title': 'Project 3',
            'description': 'Third test project',
            'image_filename': '',  # Empty image filename
            'technologies': 'Java',
            'github_link': 'https://github.com/test3',
            'demo_link': 'https://demo3.test'
        }
    ]


@pytest.fixture(autouse=True)
def mock_database_connection(test_database):
    """Mock the database connection to use the test database."""
    import DAL
    original_connect = DAL.sqlite3.connect
    
    def mock_connect(db_name):
        if db_name == "projects.db":
            return sqlite3.connect(test_database)
        return original_connect(db_name)
    
    DAL.sqlite3.connect = mock_connect
    
    yield
    
    # Restore original connect function
    DAL.sqlite3.connect = original_connect


def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add markers based on test file names
        if "test_database" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_projects" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_app" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Add slow marker for tests that might take longer
        if "database" in item.nodeid and "connection" in item.nodeid:
            item.add_marker(pytest.mark.slow)
