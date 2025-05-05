# GitPy

Python Interface to GitHub's developer API

[![name](https://codeclimate.com/github/babygame0ver/gitpy.png?style=flat-square)](https://codeclimate.com/github/babygame0ver/gitpy)
[![name](https://img.shields.io/badge/license-MIT%20License-green.svg)](https://opensource.org/licenses/MIT)
[![name](https://codecov.io/gh/akk29/gitpy/graph/badge.svg?token=nDeQuSURqF)](https://codecov.io/gh/akk29/gitpy)

## Dependencies

[![name](https://img.shields.io/badge/python-3.13.3-blue.svg?style=flat-square)](https://www.python.org/downloads/release/python-3133/)
[![name](https://img.shields.io/badge/requests-2.32.3-blue.svg?style=flat-square)](https://pypi.org/project/requests/)
[![name](https://img.shields.io/badge/coverage-7.2.7-blue.svg?style=flat-square)](https://pypi.org/project/coverage/)

## Installation

```shell

git clone https://github.com/akk29/gitpy.git
python setup.py install

```

## Features

* GitPy provide response based object for the GitHub Developer's API with the help of methods.

* Response based approach helps other Developers to write their own logic after performing the action.

* To write your own application interacting with GitHub API you need to store the end-point urls & mock them using request library. GitPy takes care it for you.

### Development Setup

1. Running Tests & Development Setup

```python
# creating and setting up environment
python -m venv .venv
.venv\scripts\activate # windows
.venv/bin/activate

# installing dependencies
pip install -r requirements.txt

# running tests
python -m unittest discover
python -m unittest tests.unit.test_repos # run specific module
python -m unittest tests.unit.test_repos.test_create_private_repository # run specific function

# generate and convert coverage report
coverage run -m unittest discover
coverage html -d coverage_html
```

## Getting Started

Gitpy works with username & token of a given account. Please obtain a personal access token with all permissions & save it somewhere securely. Refer  to
[Github Personal Token Guide](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) for more information.


## Usage Docs

Gitpy provides modules to interact with GitHub Developer API. These modules contain functions to return the response object which can be used to write your custom logic. 

Funtions are defined as per the operations.

Use exception handling provided by library in your code. See [Authentication](#authentication) example for more details

### Table of Contents


- [Authentication](#authentication)
- [Repository](#repository)
    + [create repository](#create-repository)
    + [delete repository](#delete-repository)
    + [list repositories](#delete-repository)
    + [create file](#create-file)
    + [get file details](#get-file-details)
    + [update file](#update-file)
    + [rename file](#rename-file)
    + [delete file](#delete-file)

#### Authentication
```python
from gitpy.core.auth import GitPy
from gitpy.exceptions import UnauthorizedError, ForbiddenError, ValidationError, ResourceNotFoundError

def basic_authentication():
    # bad practice use env file or environment variables to secure your credentials.
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    

    # custom error handling for all errors from github API
    try:
        result = g.authenticate()
        print(result.json())            
    except UnauthorizedError:
        print('UnauthorizedError') # putting wrong token value
        # token = 'wrong token'
        # output for UnauthorizedError       
    except ForbiddenError:
        print('ForbiddenError')
    except ResourceNotFoundError:
        print('ResourceNotFoundError')
    except ValidationError:
        print('ValidationError')
    except Exception as err:
        print('error occured',err)
    
if __name__ == '__main__':
    basic_authentication()

```

```shell
# output for UnauthorizedError

2025-05-05 17:20:10,865 - gitpy.service.loggerService - ERROR --- gitpy\service\networkService.py , get(), line no : 31 , raised UnauthorizedError() ----- api_response : {'message': 'Bad credentials', 'documentation_url': 'https://docs.github.com/rest', 'status': '401'}
UnauthorizedError
```

#### Repository

- ##### create repository

```python

"""
Repository Class deals with repository (public/private) creation/deletion.
Response based function support. 
See create_repository(gitpy_object) for more information. 
"""

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def create_repository(gitpy_object):
    repo = Repository(gitpy_object)
    response = repo.create_public_repository('my-public-repo')
    print(response.json())

    ''' or directy accessing underlying function '''
    response = repo.create_repository('my-public-repo-2',False)  # False for Public
    print(response.json())

    response = repo.create_private_repository('my-private-repo')
    print(response.json())

    ''' or directy accessing underlying function '''
    response = repo.create_repository('my-private-repo-2',True)  # True for Private
    print(response.json())

if __name__ == '__main__':
    gitpy_object = basic_authentication()
    create_repository(gitpy_object)

```

- ##### delete repository

```python
'''
Repository class deals with repository (public/private) creation/deletion.
Response based function support. 
See repo_deletion(gitpy_object,repo_name) for more information. 
'''

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def repo_deletion(gitpy_object,repo_name):
    repo = Repository(gitpy_object)
    response = repo.delete_repository(repo_name)
    print(response.status_code) # 204 -> Success , 401 -> Not Allowed , 404 -> Repo not found

if __name__ == '__main__':
    gitpy_object = basic_authentication()
    repo_deletion(gitpy_object,'my-public-repo')


 ```

- ##### list repositories
    
```python

'''
Repository class deals with repository (public/private) creation/deletion/listing.
Response based function support. 
See list_all_repos(gitpy_object) for more information. 
'''

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def list_all_repos(gitpy_object):
    repo = Repository(gitpy_object)
    response = repo.list_repositories()
    if(response.status_code == 200):
        print(json.dumps(response.json(),indent=2)) # all repo & meta-data
    else if (response.status_code == 401):        
        print('Bad credentials')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    list_all_repos(gitpy_object)
```

- ##### create file

```python

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def create_file(gitpy_object):
    repo = Repository(gitpy_object)
    repo.select_repository("test-user")
    response = repo.create_file('main4.py','import os','first file python')
    if(response.status_code == 201):
        print(json.dumps(response.json(),indent=2))
    else if (response.status_code == 422):        
        print('validation failed')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    create_file(gitpy_object)

```

- ##### get file details

```python

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def get_file_details(gitpy_object):
    repo = Repository(gitpy_object)
    repo.select_repository("test-user")
    response = repo.get_file('notes/main.py')
    if(response.status_code == 200):
        print(json.dumps(response.json(),indent=2))
    else if (response.status_code == 404):        
        print('file not found')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    get_file_details(gitpy_object)

```

- ##### update file

```python

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def udpate_file(gitpy_object):
    repo = Repository(gitpy_object)
    repo.select_repository("test-user")
    response = repo.update_file('main4.py','import os','changed file content')
    if(response.status_code == 200):
        print(json.dumps(response.json(),indent=2))
    else if (response.status_code == 404):        
        print('file not found')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    update_file(gitpy_object)

```

- ##### rename file

```python

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def rename_file(gitpy_object):
    repo = Repository(gitpy_object)
    repo.select_repository("test-user")
    response = repo.rename_file('main4.py','main5.py')
    if(response.status_code == 201):
        print(json.dumps(response.json(),indent=2))
    else if (response.status_code == 409): # Conflict         
        print('File already present')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    rename_file(gitpy_object)

```

- ##### delete file

```python

from gitpy.core.auth import GitPy
from gitpy.core.repos import Repository
import json

def basic_authentication():
    # bad practice use env file or environment variables 
    username = 'myusername'
    token = 'myrandomtoken'
    g = GitPy(username,token)    
    return g

def delete_file(gitpy_object):
    repo = Repository(gitpy_object)
    repo.select_repository("test-user")
    response = repo.delete_file('main4.py','deleted file')
    if(response.status_code == 200):
        print(json.dumps(response.json(),indent=2))
    else if (response.status_code == 404):        
        print('Resource not found')
        
if __name__ == '__main__':
    gitpy_object = basic_authentication()
    delete_file(gitpy_object)

```

 ## Support & Contribution

If you are facing issues related to bugs, code documentation, development setup or any other general issue.
Feel free to open an issue to reproduce the bug by providing sample code with proper label.   

Contributions are always welcome. You can do any of these following:

- Improve code readability, maintainability, any implemetation that makes current project better, suggest new ideas for the project.

- To make contributions : Fork the repository, implement new features by creating a seprate branch & sending PR to master branch, with writting proper unit tests.  
