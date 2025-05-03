class BASE_URL:
    API = "https://api.github.com"

CURRENT_URL = BASE_URL.API

class AUTHENTICATION_URLS:
    USER = "users/{username}"

class REPOSITORY_URLS:
    LIST_REPOS = "user/repos"
    CREATE_REPO = "user/repos"
    REPO_URL = "repos/{username}/{repo_name}"
    CREATE_FILE = "repos/{owner}/{repo}/contents/{path}"
    GET_FILE = "repos/{owner}/{repo}/contents/{path}"
    UDPATE_FILE = "repos/{owner}/{repo}/contents/{path}"
    DELETE_FILE = "repos/{owner}/{repo}/contents/{path}"


def generate_url(base_url,payload):
    return f"{CURRENT_URL}/{base_url.format(**payload)}"
