"""
Test script for database operations in the Flask website.
Tests database connection, CRUD operations, and data integrity.
"""

import pytest
import sqlite3
import os
import tempfile
from DAL import createDatabase, saveProjectDB, getAllProjects


class TestDatabase:
    """Test class for database operations."""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Create a temporary database for testing
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Store original database name and replace with test database
        self.original_db = "projects.db"
        
        # Create test database
        self.create_test_database()
        
        yield
        
        # Cleanup: remove test database file
        if os.path.exists(self.test_db.name):
            os.unlink(self.test_db.name)
    
    def create_test_database(self):
        """Create a test database with the same structure as the main database."""
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        
        # Create the projects table
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
    
    def test_database_connection(self):
        """Test that we can connect to the database."""
        conn = sqlite3.connect(self.test_db.name)
        assert conn is not None
        conn.close()
    
    def test_database_table_exists(self):
        """Test that the projects table exists and has correct structure."""
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        
        # Check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
        result = cur.fetchone()
        assert result is not None
        assert result[0] == 'projects'
        
        # Check table structure
        cur.execute("PRAGMA table_info(projects)")
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]
        
        expected_columns = ['id', 'Title', 'Description', 'ImageFileName', 'Technologies', 'GitHubLink', 'DemoLink', 'created_at']
        for expected_col in expected_columns:
            assert expected_col in column_names
        
        conn.close()
    
    def test_save_project_to_database(self):
        """Test saving a project to the database."""
        # Mock the database connection by temporarily replacing the database name
        import DAL
        original_db = DAL.sqlite3.connect
        
        def mock_connect(db_name):
            if db_name == "projects.db":
                return sqlite3.connect(self.test_db.name)
            return original_db(db_name)
        
        DAL.sqlite3.connect = mock_connect
        
        try:
            # Test data
            title = "Test Project"
            description = "This is a test project"
            image_filename = "test.png"
            technologies = "Python, Flask"
            github_link = "https://github.com/test"
            demo_link = "https://demo.test"
            
            # Save project
            saveProjectDB(title, description, image_filename, technologies, github_link, demo_link)
            
            # Verify project was saved
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            cur.execute("SELECT * FROM projects WHERE Title = ?", (title,))
            result = cur.fetchone()
            
            assert result is not None
            assert result[1] == title
            assert result[2] == description
            assert result[3] == image_filename
            assert result[4] == technologies
            assert result[5] == github_link
            assert result[6] == demo_link
            
            conn.close()
        finally:
            # Restore original connect function
            DAL.sqlite3.connect = original_db
    
    def test_get_all_projects(self):
        """Test retrieving all projects from the database."""
        # Insert test data
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        
        test_projects = [
            ("Project 1", "Description 1", "image1.png", "Tech 1", "github1", "demo1"),
            ("Project 2", "Description 2", "image2.png", "Tech 2", "github2", "demo2"),
            ("Project 3", "Description 3", "", "Tech 3", "github3", "demo3")  # Empty image
        ]
        
        for project in test_projects:
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', project)
        
        conn.commit()
        conn.close()
        
        # Mock the database connection
        import DAL
        original_db = DAL.sqlite3.connect
        
        def mock_connect(db_name):
            if db_name == "projects.db":
                return sqlite3.connect(self.test_db.name)
            return original_db(db_name)
        
        DAL.sqlite3.connect = mock_connect
        
        try:
            # Get all projects
            projects = getAllProjects()
            
            # Verify results
            assert len(projects) == 3
            assert projects[0]["Title"] == "Project 1"
            assert projects[1]["Title"] == "Project 2"
            assert projects[2]["Title"] == "Project 3"
            
            # Test placeholder image for empty image filename
            assert projects[2]["Image"] == "placeholder.png"
            
            # Verify all required fields are present
            for project in projects:
                assert "Title" in project
                assert "Description" in project
                assert "Image" in project
                assert "Technologies" in project
                assert "GitHubLink" in project
                assert "DemoLink" in project
                
        finally:
            # Restore original connect function
            DAL.sqlite3.connect = original_db
    
    def test_database_integrity(self):
        """Test database integrity constraints."""
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        
        # Test that required fields cannot be NULL
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName)
                VALUES (?, ?, ?)
            ''', (None, "Description", "image.png"))
        
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName)
                VALUES (?, ?, ?)
            ''', ("Title", None, "image.png"))
        
        with pytest.raises(sqlite3.IntegrityError):
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName)
                VALUES (?, ?, ?)
            ''', ("Title", "Description", None))
        
        conn.close()
    
    def test_database_auto_increment(self):
        """Test that the ID field auto-increments correctly."""
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        
        # Insert two projects
        cur.execute('''
            INSERT INTO projects (Title, Description, ImageFileName)
            VALUES (?, ?, ?)
        ''', ("Project 1", "Description 1", "image1.png"))
        
        cur.execute('''
            INSERT INTO projects (Title, Description, ImageFileName)
            VALUES (?, ?, ?)
        ''', ("Project 2", "Description 2", "image2.png"))
        
        conn.commit()
        
        # Check IDs
        cur.execute("SELECT id FROM projects ORDER BY id")
        ids = [row[0] for row in cur.fetchall()]
        
        assert ids == [1, 2]
        
        conn.close()
