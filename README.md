# GitPy

Python Interface to GitHub's developer API

[![Python](https://img.shields.io/badge/Python-3.13.3-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3133/)
[![License](https://img.shields.io/badge/license-MIT%20License-green.svg)](https://opensource.org/licenses/MIT)
[![Maintainability](https://qlty.sh/gh/akk29/projects/gitpy/maintainability.png)](https://qlty.sh/gh/akk29/projects/gitpy)
[![Coverage](https://codecov.io/gh/akk29/gitpy/graph/badge.svg?token=nDeQuSURqF)](https://codecov.io/gh/akk29/gitpy)


A lightweight, response-based Python SDK designed to streamline interactions with the GitHub Developer API.

## Installation

```shell
git clone https://github.com/akk29/gitpy.git
cd gitpy
python setup.py install
```

## Features

* GitPy provide response based object for the GitHub Developer's API with the help of methods.

* Response based approach helps other Developers to write their own logic after performing the action.

* To write your own application interacting with GitHub API you need to store the end-point urls & mock them using request library. GitPy takes care it for you.


## Documentation


### Getting Started

GitPy requires your GitHub username and a Personal Access Token (PAT). Securely obtain a token with the appropriate scopes by following the [GitHub Personal Access Token Guide](https://github.com).

---

### Technical Architecture & Core Usage

#### 1. Robust Authentication & Error Handling
Always secure your credentials using environment variables or a `.env` file rather than hardcoding credentials into your execution script.

```python
import os
from gitpy.core.auth import GitPy
from gitpy.exceptions import (
    UnauthorizedError, 
    ForbiddenError, 
    ValidationError, 
    ResourceNotFoundError
)

def initialize_client():
    """Initializes the GitPy client using secure environment variables."""
    username = os.getenv("GITHUB_USERNAME", "default_user")
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise ValueError("Critical Error: GITHUB_TOKEN environment variable is not set.")
        
    return GitPy(username, token)

def run_authentication_check():
    client = initialize_client()
    try:
        result = client.authenticate()
        print(f"Authentication Successful: {result.json()}")            
    except UnauthorizedError:
        print("Error 401: Unauthorized access. Please verify your token credentials.")
    except ForbiddenError:
        print("Error 403: Forbidden. Rate limit exceeded or insufficient scopes.")
    except ResourceNotFoundError:
        print("Error 404: Resource not found.")
    except ValidationError:
        print("Error 422: Validation failed.")
    except Exception as err:
        print(f"An unexpected networking error occurred: {err}")

if __name__ == '__main__':
    run_authentication_check()
```

#### 2. Repository Operations
The `Repository` class abstractly handles creating, deleting, and listing your remote targets.

```python
from gitpy.core.repos import Repository
# Assumes client initialization logic from the authentication block above
client = initialize_client()
repo_manager = Repository(client)

# Create Public and Private Repositories
pub_repo = repo_manager.create_public_repository('my-public-repo')
priv_repo = repo_manager.create_private_repository('my-private-repo')

# Direct boolean routing: (repo_name, is_private)
custom_repo = repo_manager.create_repository('custom-repo', is_private=True)

# List all accessible repositories
repo_list_response = repo_manager.list_repositories()
if repo_list_response.status_code == 200:
    print(repo_list_response.json())

# Delete a target repository
delete_response = repo_manager.delete_repository('my-public-repo')
# Status mappings: 204 = Success, 401 = Not Allowed, 404 = Not Found
print(f"Deletion status: {delete_response.status_code}") 
```

#### 3. File System & Content Management
Before performing CRUD operations on individual files, you must explicitly bind your manager to a designated target project via `.select_repository()`.

```python
import json
from gitpy.core.repos import Repository

client = initialize_client()
file_manager = Repository(client)
file_manager.select_repository("target-project-name")

# Create a File
res_create = file_manager.create_file('main.py', 'import os', 'initial commit message')
if res_create.status_code == 201:
    print("File provisioned successfully.")

# Read File Metadata/Details
res_get = file_manager.get_file('notes/main.py')
if res_get.status_code == 200:
    print(json.dumps(res_get.json(), indent=2))

# Update File Content
res_update = file_manager.update_file('main.py', 'import os\nprint("Hello World")', 'updated execution logic')

# Rename/Move File
res_rename = file_manager.rename_file('main.py', 'app.py')

# Delete File
res_delete = file_manager.delete_file('app.py', 'purged legacy scripts')
```
---
