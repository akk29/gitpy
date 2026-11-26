# GitPy

Python interface to the GitHub REST API.

[![Python](https://img.shields.io/badge/Python-3.13.3-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3133/)
[![License](https://img.shields.io/badge/license-MIT%20License-green.svg)](https://opensource.org/licenses/MIT)
[![Maintainability](https://qlty.sh/gh/akk29/projects/gitpy/maintainability.png)](https://qlty.sh/gh/akk29/projects/gitpy)
[![Coverage](https://codecov.io/gh/akk29/gitpy/graph/badge.svg?token=nDeQuSURqF)](https://codecov.io/gh/akk29/gitpy)

GitPy is a lightweight, response-based client that handles GitHub API endpoints
and returns `requests.Response` objects for application-specific logic.

## Installation

```shell
git clone https://github.com/akk29/gitpy.git
cd gitpy
python -m venv .venv
```

Activate the virtual environment.

macOS / Linux:
```shell
source .venv/bin/activate
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt:
```bat
.\.venv\Scripts\activate.bat
```

Install GitPy and its dependencies in the active environment:
```shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

GitPy is a Python library, not a standalone application. With the virtual
environment active and credentials configured, put your GitPy code in a
Python file (for example, `example.py`) and run it with:

```shell
python example.py
```

## Running tests

Run the test suite with pytest:
```shell
python -m pytest
```

Alternatively, run the standard-library unittest suite:
```shell
python -m unittest discover
```

To collect coverage:
```shell
coverage run -m unittest discover
```

## Getting started

GitPy requires a GitHub username and a Personal Access Token. Configure them
through environment variables; never commit credentials to source control.

```shell
export GITHUB_USERNAME="your-github-username"
export GITHUB_TOKEN="github_pat_your_token"
```

On Windows PowerShell:

```powershell
$env:GITHUB_USERNAME = "your-github-username"
$env:GITHUB_TOKEN = "github_pat_your_token"
```

Use only the Personal Access Token scopes required by the operations you run.
Private repository operations normally require `repo` scope for a classic
token. Fine-grained tokens should be limited to the necessary repositories
and permissions.

## Authentication

```python
import os

from gitpy.core.auth import GitPy

github = GitPy(
    username=os.environ["GITHUB_USERNAME"],
    token=os.environ["GITHUB_TOKEN"],
)

response = github.authenticate()
print(response.status_code)
print(response.json()["login"])
```

`authenticate()` sends `GET /user` and stores the authenticated user's JSON
details in `github.user_details`.

### Authentication error handling

```python
from gitpy.exceptions import (
    ForbiddenError,
    ResourceNotFoundError,
    UnauthorizedError,
    ValidationError,
)

try:
    github.authenticate()
except UnauthorizedError:
    print("The token is missing or invalid.")
except ForbiddenError:
    print("Access is forbidden or the token lacks required scopes.")
except ResourceNotFoundError:
    print("The requested GitHub resource was not found.")
except ValidationError:
    print("GitHub rejected the request payload.")
```

## Repository operations

Create a repository manager from an authenticated `GitPy` instance:

```python
from gitpy.core.repos import Repository

github.authenticate()
repositories = Repository(github)
```

### Create repositories

```python
public_response = repositories.create_public_repository("public-example")
private_response = repositories.create_private_repository("private-example")

# Explicit form: create_repository(name, access)
other_response = repositories.create_repository("other-example", access=True)
```

Successful creation usually returns HTTP `201`. It also selects the newly
created repository as the current repository.

### List repositories

```python
response = repositories.list_repositories()

if response.status_code == 200:
    for repository in response.json():
        print(repository["full_name"], repository["private"])
```

### Delete a repository

```python
response = repositories.delete_repository("public-example")

if response.status_code == 204:
    print("Repository deleted.")
```

Repository deletion is permanent.

## File operations

Select the repository before accessing repository files:

```python
repositories.select_repository("example-project")
```

```python
# Create a file
response = repositories.create_file(
    "src/main.py",
    'print("Hello")\n',
    "Add main program",
)

# Get file details
response = repositories.get_file("src/main.py")

# Update a file
response = repositories.update_file(
    "src/main.py",
    'print("Hello, GitHub")\n',
    "Update main program",
)

# Rename a file
response = repositories.rename_file("src/main.py", "src/app.py")

# Delete a file
response = repositories.delete_file(
    "src/app.py",
    "Remove obsolete application file",
)
```

GitPy encodes text file content as base64 automatically. GitHub's API has no
dedicated rename operation, so `rename_file()` creates the destination and
deletes the source. Both operations create separate commits.

## API reference

### `GitPy(username=None, token=None)`

The authenticated client.

Attributes:

- `username`: GitHub username
- `token`: Personal Access Token
- `network_service`: HTTP session and request handler
- `user_details`: authenticated user JSON after `authenticate()`

Methods:

- `authenticate()`: sends `GET /user` and returns `requests.Response`

### `Repository(authenticated_obj)`

The repository and file operations manager. It requires a `GitPy` instance.

| Method | HTTP operation | Result |
| --- | --- | --- |
| `list_repositories()` | `GET /user/repos` | `requests.Response` |
| `create_repository(repo_name, access)` | `POST /user/repos` | `requests.Response` |
| `create_public_repository(repo_name)` | Creates a public repository | `requests.Response` |
| `create_private_repository(repo_name)` | Creates a private repository | `requests.Response` |
| `delete_repository(repo_name)` | `DELETE /repos/{username}/{repo_name}` | `requests.Response` |
| `select_repository(repo_name)` | Sets the current repository | `None` |
| `create_file(abs_path, content, msg)` | `PUT /repos/{owner}/{repo}/contents/{path}` | `requests.Response` |
| `get_file(abs_path)` | `GET /repos/{owner}/{repo}/contents/{path}` | `requests.Response` |
| `update_file(abs_path, content, msg)` | Gets the SHA, then updates file contents | `requests.Response` or `None` |
| `rename_file(current, new)` | Creates the destination, then deletes the source | `None` |
| `delete_file(abs_path, msg)` | Gets the SHA, then deletes file contents | `requests.Response` or `None` |

## Exceptions

GitPy raises exceptions for HTTP error responses:

| HTTP status | Exception | Meaning |
| --- | --- | --- |
| 401 | `UnauthorizedError` | Token is missing or invalid |
| 403 | `ForbiddenError` | Access denied or insufficient scope |
| 404 | `ResourceNotFoundError` | Repository or file was not found |
| 409 | `ConflictError` | Resource state conflicts with the request |
| 422 | `ValidationError` | GitHub rejected or could not validate the request |
| 503 | `ServiceUnavailableError` | GitHub service is unavailable |

Exception instances expose `response` and `code`:

```python
from gitpy.exceptions import ForbiddenError

try:
    repositories.list_repositories()
except ForbiddenError as error:
    print(error.code)
    print(error.response)
```

Request transport failures raise `RequestLibraryError`. The HTTP and transport
exception classes are in `gitpy.exceptions`.

## License

GitPy is distributed under the [MIT License](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and contribution
guidelines.
