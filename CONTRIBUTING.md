# Contributing

Contributions are welcome. For bugs or feature requests, open an issue with
steps to reproduce or a clear description of the proposed change. For code
changes, fork the repository, create a branch, and open a pull request against
`main`. Include focused tests for behavior you change.

## Development setup

From the repository root, create and activate a virtual environment.

macOS / Linux:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies and the local package:

```shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Tests

Run the full test suite:

```shell
python -m pytest
```

Run a specific test module or test case:

```shell
python -m unittest tests.unit.test_repos
python -m unittest tests.unit.test_repos.TestRepository.test_create_private_repository
```

Generate a coverage report:

```shell
coverage run -m unittest discover
coverage html -d coverage_html
```
