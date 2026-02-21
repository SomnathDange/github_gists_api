"""GitHub Gists API - Fetch public gists for any GitHub user."""

import requests
from flask import Flask, jsonify, request  # jsonify converts Python dict/list to JSON response

app = Flask(__name__)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy'})


@app.route('/version')
def version():
    """API version endpoint."""
    return jsonify({'version': '1.0.0', 'api': 'GitHub Gists API'})


@app.route('/<username>/<reponame>')
def get_repo(username, reponame):
    """Fetch repository details.
    
    Args:
        username: GitHub username
        reponame: Repository name
        
    Returns:
        JSON with repo details
    """
    url = f'https://api.github.com/repos/{username}/{reponame}'
    response = requests.get(url)
    
    if response.status_code == 404:
        return jsonify({'error': 'Repository not found'}), 404
    
    if response.status_code != 200:
        return jsonify({'error': 'GitHub API error'}), 500
    
    repo = response.json()
    return jsonify({
        'name': repo['name'],
        'description': repo['description'],
        'url': repo['html_url'],
        'stars': repo['stargazers_count'],
        'forks': repo['forks_count'],
        'language': repo['language']
    })


@app.route('/<username>')
def get_gists(username):
    """Fetch and return public gists for a GitHub user.
    
    Args:
        username: GitHub username from URL path
        
    Query Parameters:
        page: Page number (default: 1)
        per_page: 30
        
    Returns:
        JSON list of gists with id, description, url, and files
        
    Error Responses:
        404: User not found
        500: GitHub API error
    """
    # Get pagination params
    page = request.args.get('page', 1, type=int)
    per_page = 30
    
    # GitHub API endpoint with pagination
    url = f'https://api.github.com/users/{username}/gists'
    params = {'page': page, 'per_page': per_page}
    
    # Fetch gists from GitHub
    response = requests.get(url, params=params)
    
    # Handle user not found
    if response.status_code == 404:
        return jsonify({'error': 'User not found'}), 404
    
    # Handle other API errors
    if response.status_code != 200:
        return jsonify({'error': 'GitHub API error'}), 500
    
    # Parse and format gist data
    gists = response.json()
    
    # Check if user exists but has no gists
    if len(gists) == 0:
        return jsonify({'error': 'No gists found for this user'}), 404
    
    result = []
    
    for gist in gists:
        result.append({
            'id': gist['id'],
            'description': gist['description'],
            'url': gist['html_url'],
            'files': list(gist['files'].keys())
        })
    
    return jsonify(result)


if __name__ == '__main__':
    # Run server on all interfaces, port 8080
    # Debug mode OFF for production security
    app.run(host='0.0.0.0', port=8080, debug=False)
