"""Test suite for GitHub Gists API.

Tests validate:
- Successful gist retrieval for valid users
- Proper error handling for invalid users
- Response structure and data format
- Pagination functionality
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app.
    
    Yields:
        Flask test client configured for testing
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_gists_for_octocat(client):
    """Test successful gist retrieval for the 'octocat' user.
    
    Validates:
    - 200 status code
    - Response is a list
    - List contains gist data
    - Each gist has required fields
    """
    response = client.get('/octocat')
    
    # Check successful response
    assert response.status_code == 200
    
    # Validate response structure
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Validate each gist has required fields
    for gist in data:
        assert 'id' in gist
        assert 'description' in gist
        assert 'url' in gist
        assert 'files' in gist


def test_user_not_found(client):
    """Test error handling for non-existent user.
    
    Validates:
    - 404 status code
    - Error message in response
    """
    response = client.get('/thisuserdoesnotexist12345xyz')
    
    # Check 404 response
    assert response.status_code == 404
    
    # Validate error message
    data = response.get_json()
    assert 'error' in data


def test_pagination(client):
    """Test pagination parameters.
    
    Validates:
    - Page parameter works
    - Returns valid response
    """
    response = client.get('/octocat?page=1')
    
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_health_endpoint(client):
    """Test /health endpoint."""
    response = client.get('/health')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'status' in data
    assert data['status'] == 'healthy'


def test_version_endpoint(client):
    """Test /version endpoint."""
    response = client.get('/version')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'version' in data
    assert 'api' in data
    assert data['version'] == '1.0.0'


def test_get_repo(client):
    """Test /<username>/<reponame> endpoint."""
    response = client.get('/octocat/Hello-World')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'name' in data
    assert 'description' in data
    assert 'url' in data
    assert 'stars' in data
    assert 'forks' in data


def test_repo_not_found(client):
    """Test repo not found error."""
    response = client.get('/octocat/nonexistentrepo12345')
    
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
