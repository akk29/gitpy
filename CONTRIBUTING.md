# Development Setup

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

# Support & Contribution

If you are facing issues related to bugs, code [documentation]((https://github.com/akk29/gitpy/wiki)), development setup or any other general issue.
Feel free to open an issue to reproduce the bug by providing sample code with proper label.   

Contributions are always welcome. You can do any of these following:

- Improve code readability, maintainability, any implemetation that makes current project better, suggest new ideas for the project.

- To make contributions : Fork the repository, implement new features by creating a seprate branch & sending PR to master branch, with writting proper unit tests.  