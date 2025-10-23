"""
Test script for project-related functionality in the Flask website.
Tests project data validation, formatting, and business logic.
"""

import pytest
import tempfile
import os
import sqlite3
from DAL import saveProjectDB, getAllProjects


class TestProjects:
    """Test class for project-related functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Create a temporary database for testing
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
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
    
    def mock_database_connection(self):
        """Mock the database connection to use test database."""
        import DAL
        original_connect = DAL.sqlite3.connect
        
        def mock_connect(db_name):
            if db_name == "projects.db":
                return sqlite3.connect(self.test_db.name)
            return original_connect(db_name)
        
        DAL.sqlite3.connect = mock_connect
        return original_connect
    
    def test_save_project_with_all_fields(self):
        """Test saving a project with all fields populated."""
        original_connect = self.mock_database_connection()
        
        try:
            # Test data with all fields
            title = "Complete Project"
            description = "A comprehensive project with all fields"
            image_filename = "complete_project.png"
            technologies = "Python, Flask, SQLite, HTML, CSS"
            github_link = "https://github.com/user/complete-project"
            demo_link = "https://demo.example.com/complete-project"
            
            # Save project
            saveProjectDB(title, description, image_filename, technologies, github_link, demo_link)
            
            # Verify project was saved correctly
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
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_save_project_with_minimal_fields(self):
        """Test saving a project with only required fields."""
        original_connect = self.mock_database_connection()
        
        try:
            # Test data with only required fields
            title = "Minimal Project"
            description = "A project with only required fields"
            image_filename = "minimal.png"
            
            # Save project with empty optional fields
            saveProjectDB(title, description, image_filename, "", "", "")
            
            # Verify project was saved correctly
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            cur.execute("SELECT * FROM projects WHERE Title = ?", (title,))
            result = cur.fetchone()
            
            assert result is not None
            assert result[1] == title
            assert result[2] == description
            assert result[3] == image_filename
            assert result[4] == ""  # Technologies
            assert result[5] == ""  # GitHub Link
            assert result[6] == ""  # Demo Link
            
            conn.close()
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_get_projects_with_placeholder_images(self):
        """Test that projects with empty image filenames get placeholder images."""
        original_connect = self.mock_database_connection()
        
        try:
            # Insert test data with empty image filename
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("Test Project", "Test Description", "", "Python", "https://github.com/test", "https://demo.test"))
            
            conn.commit()
            conn.close()
            
            # Get all projects
            projects = getAllProjects()
            
            # Verify placeholder image is used
            assert len(projects) == 1
            assert projects[0]["Image"] == "placeholder.png"
            assert projects[0]["Title"] == "Test Project"
            assert projects[0]["Description"] == "Test Description"
            
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_get_projects_with_none_values(self):
        """Test handling of None values in database fields."""
        original_connect = self.mock_database_connection()
        
        try:
            # Insert test data with None values
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("Test Project", "Test Description", "test.png", None, None, None))
            
            conn.commit()
            conn.close()
            
            # Get all projects
            projects = getAllProjects()
            
            # Verify None values are handled correctly
            assert len(projects) == 1
            project = projects[0]
            assert project["Technologies"] == ""
            assert project["GitHubLink"] == ""
            assert project["DemoLink"] == ""
            
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_multiple_projects_retrieval(self):
        """Test retrieving multiple projects from the database."""
        original_connect = self.mock_database_connection()
        
        try:
            # Insert multiple test projects
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            
            test_projects = [
                ("Project A", "Description A", "image_a.png", "Python", "github_a", "demo_a"),
                ("Project B", "Description B", "image_b.png", "JavaScript", "github_b", "demo_b"),
                ("Project C", "Description C", "", "Java", "github_c", "demo_c")  # Empty image
            ]
            
            for project in test_projects:
                cur.execute('''
                    INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', project)
            
            conn.commit()
            conn.close()
            
            # Get all projects
            projects = getAllProjects()
            
            # Verify all projects are retrieved
            assert len(projects) == 3
            
            # Verify each project has correct data
            titles = [p["Title"] for p in projects]
            assert "Project A" in titles
            assert "Project B" in titles
            assert "Project C" in titles
            
            # Verify placeholder image for Project C
            project_c = next(p for p in projects if p["Title"] == "Project C")
            assert project_c["Image"] == "placeholder.png"
            
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_project_data_structure(self):
        """Test that project data has the expected structure."""
        original_connect = self.mock_database_connection()
        
        try:
            # Insert a test project
            conn = sqlite3.connect(self.test_db.name)
            cur = conn.cursor()
            
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("Test Project", "Test Description", "test.png", "Python, Flask", "https://github.com/test", "https://demo.test"))
            
            conn.commit()
            conn.close()
            
            # Get all projects
            projects = getAllProjects()
            
            # Verify data structure
            assert len(projects) == 1
            project = projects[0]
            
            # Check all required keys are present
            required_keys = ["Title", "Description", "Image", "Technologies", "GitHubLink", "DemoLink"]
            for key in required_keys:
                assert key in project
            
            # Check data types
            assert isinstance(project["Title"], str)
            assert isinstance(project["Description"], str)
            assert isinstance(project["Image"], str)
            assert isinstance(project["Technologies"], str)
            assert isinstance(project["GitHubLink"], str)
            assert isinstance(project["DemoLink"], str)
            
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
    
    def test_empty_database_returns_empty_list(self):
        """Test that an empty database returns an empty list."""
        original_connect = self.mock_database_connection()
        
        try:
            # Get all projects from empty database
            projects = getAllProjects()
            
            # Verify empty list is returned
            assert isinstance(projects, list)
            assert len(projects) == 0
            
        finally:
            # Restore original connect function
            import DAL
            DAL.sqlite3.connect = original_connect
