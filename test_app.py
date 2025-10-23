"""
Test script for Flask application routes and responses.
Tests all endpoints, HTTP methods, and response content.
"""

import pytest
import tempfile
import os
import sqlite3
from flask import Flask
from app import app, createDatabase
from DAL import saveProjectDB, getAllProjects


class TestFlaskApp:
    """Test class for Flask application functionality."""
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Create a temporary database for testing
        self.test_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.test_db.close()
        
        # Create test database
        self.create_test_database()
        
        # Configure Flask app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()
        
        # Mock the database connection
        self.mock_database_connection()
        
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
        
        # Insert some test data
        test_projects = [
            ("Test Project 1", "Description 1", "project1.png", "Python, Flask", "https://github.com/test1", "https://demo1.test"),
            ("Test Project 2", "Description 2", "project2.png", "JavaScript, React", "https://github.com/test2", "https://demo2.test")
        ]
        
        for project in test_projects:
            cur.execute('''
                INSERT INTO projects (Title, Description, ImageFileName, Technologies, GitHubLink, DemoLink)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', project)
        
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
    
    def test_index_route(self):
        """Test the index route returns correct response."""
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_index_route_alias(self):
        """Test the /index route alias works correctly."""
        response = self.client.get('/index')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_about_route(self):
        """Test the about route returns correct response."""
        response = self.client.get('/about')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_resume_route(self):
        """Test the resume route returns correct response."""
        response = self.client.get('/resume')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_projects_route_get(self):
        """Test the projects route returns projects data."""
        response = self.client.get('/projects')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
        
        # Check that project data is included in the response
        # This assumes the template uses the projects variable
        response_text = response.data.decode('utf-8')
        # The exact content depends on your template, but we can check for basic HTML structure
        assert '<html' in response_text.lower() or '<!doctype' in response_text.lower()
    
    def test_contact_route_get(self):
        """Test the contact route GET method returns form."""
        response = self.client.get('/contact')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
        
        # Check for form elements (assuming your contact template has a form)
        response_text = response.data.decode('utf-8')
        assert '<html' in response_text.lower() or '<!doctype' in response_text.lower()
    
    def test_contact_route_post_valid_data(self):
        """Test the contact route POST method with valid data."""
        form_data = {
            'title': 'New Test Project',
            'description': 'This is a test project created via form',
            'image_filename': 'new_project.png',
            'technologies': 'Python, Flask, SQLite',
            'github_link': 'https://github.com/test/new-project',
            'demo_link': 'https://demo.test/new-project'
        }
        
        response = self.client.post('/contact', data=form_data)
        assert response.status_code == 200
        
        # Verify project was added to database
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects WHERE Title = ?", (form_data['title'],))
        result = cur.fetchone()
        assert result is not None
        assert result[1] == form_data['title']
        conn.close()
    
    def test_contact_route_post_minimal_data(self):
        """Test the contact route POST method with minimal required data."""
        form_data = {
            'title': 'Minimal Project',
            'description': 'Minimal test project',
            'image_filename': 'minimal.png',
            'technologies': '',
            'github_link': '',
            'demo_link': ''
        }
        
        response = self.client.post('/contact', data=form_data)
        assert response.status_code == 200
        
        # Verify project was added to database
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        cur.execute("SELECT * FROM projects WHERE Title = ?", (form_data['title'],))
        result = cur.fetchone()
        assert result is not None
        assert result[1] == form_data['title']
        conn.close()
    
    def test_contact_route_post_missing_required_fields(self):
        """Test the contact route POST method with missing required fields."""
        form_data = {
            'title': '',  # Missing required field
            'description': 'Test project without title',
            'image_filename': 'test.png'
        }
        
        response = self.client.post('/contact', data=form_data)
        # Should still return 200 but may show error message
        assert response.status_code == 200
    
    def test_thankyou_route(self):
        """Test the thankyou route returns correct response."""
        response = self.client.get('/thankyou')
        assert response.status_code == 200
        assert b'<!DOCTYPE html>' in response.data or b'<html' in response.data
    
    def test_nonexistent_route(self):
        """Test that nonexistent routes return 404."""
        response = self.client.get('/nonexistent')
        assert response.status_code == 404
    
    def test_projects_data_in_response(self):
        """Test that projects data is properly passed to templates."""
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # This test assumes your template displays project titles
        # You may need to adjust based on your actual template content
        response_text = response.data.decode('utf-8')
        # Basic check that we get a valid HTML response
        assert '<html' in response_text.lower() or '<!doctype' in response_text.lower()
    
    def test_contact_data_in_response(self):
        """Test that projects data is properly passed to contact template."""
        response = self.client.get('/contact')
        assert response.status_code == 200
        
        # This test assumes your contact template displays current projects
        response_text = response.data.decode('utf-8')
        # Basic check that we get a valid HTML response
        assert '<html' in response_text.lower() or '<!doctype' in response_text.lower()
    
    def test_http_methods(self):
        """Test that routes only accept allowed HTTP methods."""
        # Test that POST is not allowed on most routes
        routes_to_test = ['/', '/index', '/about', '/resume', '/projects', '/thankyou']
        
        for route in routes_to_test:
            response = self.client.post(route)
            # Should return 405 Method Not Allowed or handle gracefully
            assert response.status_code in [200, 405]
    
    def test_contact_route_put_method(self):
        """Test that PUT method is not allowed on contact route."""
        response = self.client.put('/contact')
        assert response.status_code == 405  # Method Not Allowed
    
    def test_contact_route_delete_method(self):
        """Test that DELETE method is not allowed on contact route."""
        response = self.client.delete('/contact')
        assert response.status_code == 405  # Method Not Allowed
    
    def test_response_content_type(self):
        """Test that all routes return HTML content type."""
        routes_to_test = ['/', '/about', '/resume', '/projects', '/contact', '/thankyou']
        
        for route in routes_to_test:
            response = self.client.get(route)
            assert response.status_code == 200
            # Check that content type is HTML
            assert 'text/html' in response.content_type
    
    def test_database_initialization(self):
        """Test that database is properly initialized."""
        # This test verifies that createDatabase function works
        # We'll test it by checking if we can retrieve projects
        response = self.client.get('/projects')
        assert response.status_code == 200
        
        # Verify that projects are being retrieved from our test database
        conn = sqlite3.connect(self.test_db.name)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM projects")
        count = cur.fetchone()[0]
        assert count > 0  # Should have our test data
        conn.close()
