class AUTHENTICATION_URLS:
    USER = "users/{username}"

class REPOSITORY_URLS:
    LIST_REPOS = "user/repos"
    CREATE_REPO = "user/repos"
    REPO_URL = "repos/{username}/{repo_name}"


def generate_url(base_url,payload):
    return base_url.format(**payload)
