# Flask Website Test Suite

This directory contains comprehensive test scripts for the Flask personal website project. The test suite ensures that all functionality works correctly before deployment.

## Test Files

### `test_database.py`
Tests database operations and data integrity:
- Database connection and table creation
- CRUD operations (Create, Read, Update, Delete)
- Data validation and constraints
- Auto-increment functionality
- Error handling

### `test_projects.py`
Tests project-related functionality:
- Project data validation
- Image placeholder handling
- Multiple project retrieval
- Data structure validation
- Empty database handling

### `test_app.py`
Tests Flask application routes and responses:
- All HTTP routes (`/`, `/about`, `/resume`, `/projects`, `/contact`, `/thankyou`)
- HTTP methods (GET, POST)
- Form submission and validation
- Response content and status codes
- Error handling

## Configuration Files

### `pytest.ini`
Pytest configuration with:
- Test discovery patterns
- Coverage reporting
- Custom markers for test categorization
- Output formatting options

### `conftest.py`
Shared fixtures and test configuration:
- Test database setup and teardown
- Flask app test client
- Sample data fixtures
- Database connection mocking

### `run_tests.py`
Convenient test runner script with multiple configurations:
- All tests with verbose output
- Unit tests only
- Integration tests only
- Coverage reports
- Individual test file execution

## GitHub Actions

### `.github/workflows/test.yml`
Automated testing on GitHub:
- Runs on push and pull requests
- Tests against multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Generates coverage reports
- Uploads results to Codecov

## Running Tests

### Prerequisites
Install test dependencies:
```bash
pip install -r requirements.txt
```

### Basic Test Execution
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_database.py

# Run specific test function
pytest test_database.py::TestDatabase::test_database_connection
```

### Using the Test Runner
```bash
# Run all test configurations
python run_tests.py

# Make the script executable (Linux/Mac)
chmod +x run_tests.py
./run_tests.py
```

### Test Categories
```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"
```

### Coverage Reports
```bash
# Generate terminal coverage report
pytest --cov=. --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=. --cov-report=html:htmlcov

# Open HTML report (after generation)
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

## Test Structure

### Test Classes
- `TestDatabase`: Database operation tests
- `TestProjects`: Project functionality tests  
- `TestFlaskApp`: Flask application tests

### Test Functions
All test functions follow the naming convention `test_*` and test specific functionality:
- `test_database_connection()`: Verifies database connectivity
- `test_save_project_to_database()`: Tests project creation
- `test_get_all_projects()`: Tests project retrieval
- `test_index_route()`: Tests homepage route
- `test_contact_route_post()`: Tests form submission

### Fixtures
- `setup_and_teardown`: Database setup/cleanup for each test
- `test_database`: Temporary test database for the session
- `flask_app`: Flask app instance for testing
- `client`: Test client for making HTTP requests
- `sample_project_data`: Sample data for testing

## Best Practices

### Test Isolation
- Each test uses a temporary database
- Tests don't depend on each other
- Clean setup and teardown for each test

### Mocking
- Database connections are mocked to use test database
- No external dependencies in tests
- Predictable test environment

### Coverage
- Aim for high test coverage (>90%)
- Test both success and error cases
- Include edge cases and boundary conditions

### Documentation
- Clear test names describing what is being tested
- Comments explaining complex test logic
- README with usage instructions

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure you're running tests from the project root directory
   - Check that all dependencies are installed

2. **Database Errors**
   - Tests use temporary databases, so no cleanup needed
   - Check that SQLite is available

3. **Flask App Errors**
   - Ensure `app.py` is in the current directory
   - Check that all routes are properly defined

4. **Coverage Issues**
   - Some files may not be covered if they're not imported during tests
   - Check the HTML coverage report for detailed information

### Debug Mode
Run tests with extra debugging information:
```bash
pytest -v -s --tb=long
```

### Verbose Output
Get detailed test output:
```bash
pytest -v --tb=short
```

## Contributing

When adding new features:
1. Write tests first (TDD approach)
2. Ensure all tests pass
3. Maintain or improve test coverage
4. Update this README if needed

When fixing bugs:
1. Write a test that reproduces the bug
2. Fix the bug
3. Ensure the test passes
4. Run the full test suite
